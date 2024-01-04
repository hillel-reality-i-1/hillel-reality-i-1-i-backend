import json
from django.http import JsonResponse
import requests
from allauth.account.models import EmailAddress
from django.contrib.auth import login
from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.views.decorators.http import require_POST

# from apps.base.utils import get_frontend_url
from apps.users.models import User
from django.urls import reverse


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(require_POST, name="post")
class SocialLoginView(View):
    def post(self, request, *args, **kwargs):
        access_token = request.POST.get("access_token")

        # Data parsing from access token
        url = f"https://oauth2.googleapis.com/tokeninfo?access_token={access_token}"
        response = requests.get(url)
        user_data_token = response.json()

        response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", params={"access_token": access_token})

        user_data = response.json()
        user_data.update(user_data_token)

        if not user_data.get("email"):
            return JsonResponse({"detail": "Email is missing in user_data", "user_data": user_data}, status=400)

        user, created = User.objects.get_or_create(email=user_data["email"])
        if created:
            user.set_unusable_password()
            user.save()

        # Create/update SocialAccount
        SocialAccount.objects.update_or_create(
            user=user, provider="google", defaults={"uid": user_data.get("sub", ""), "extra_data": {**user_data}}
        )

        # Create EmailAddress
        email, created = EmailAddress.objects.get_or_create(
            user=user,
            email=user_data["email"],
            defaults={
                "primary": True,
                "verified": True,
            },
        )

        if not created and not email.verified:
            email.verified = True
            email.save()

        # User login
        login(request, user, backend="allauth.account.auth_backends.AuthenticationBackend")

        token, created = Token.objects.get_or_create(user=user)

        # Create JSON response with token and redirect_url
        response_data = {
            "token": token.key,
            "redirect_url": reverse("front_create_profile_from_social_account", args=[*args])
            if user.full_name == "Anonim User"
            else reverse("front_home", args=[*args]),  # get_frontend_url("front_home"),
        }

        # Create HTTP response with JSON data and redirect
        response = HttpResponse(json.dumps(response_data), content_type="application/json")
        # if created:
        #     response["Location"] = get_frontend_url("front_create_profile_from_social_account")  # request.path_info
        # else:
        #     response["Location"] = get_frontend_url("front_home")  # Redirect to the main page

        return response
