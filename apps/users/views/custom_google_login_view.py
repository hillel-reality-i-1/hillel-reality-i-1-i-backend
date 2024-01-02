import json
from django.http import JsonResponse
import requests
from allauth.account.models import EmailAddress
from django.contrib.auth import login
from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from apps.users.models import User


@method_decorator(csrf_exempt, name="dispatch")
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
            return JsonResponse({"detail": "Email is missing in user_data"}, status=400)

        # Create user
        users = User.objects.filter(email=user_data["email"])
        if not users:
            user = User.objects.create(
                email=user_data["email"],
            )
            user.set_unusable_password()
            user.save()
        else:
            user = users[0]

        # Create/update SocialAccount
        SocialAccount.objects.update_or_create(
            user=user, provider="google", defaults={"uid": user_data.get("sub", ""), "extra_data": {**user_data}}
        )

        # Create EmailAddress
        emails = EmailAddress.objects.filter(user=user)
        if not emails:
            EmailAddress.objects.create(user=user, email=user_data["email"], primary=True, verified=True)
        else:
            if not emails[0].verified:
                emails[0].verified = True
                emails[0].save()

        # User login
        login(request, user, backend="allauth.account.auth_backends.AuthenticationBackend")

        token, created = Token.objects.get_or_create(user=user)

        # Create JSON response with token
        response_data = {"token": token.key}

        # Create HTTP response with JSON data and redirect
        response = HttpResponse(json.dumps(response_data), content_type="application/json")
        if not users:
            response["Location"] = "http://dmytromigirov.space:3000/createUnAccount/"  # request.path_info
        else:
            response["Location"] = "/"  # Redirect to the main page

        return response
