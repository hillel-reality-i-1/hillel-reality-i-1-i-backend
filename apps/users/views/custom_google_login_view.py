import requests
from allauth.account.models import EmailAddress
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from allauth.socialaccount.models import SocialAccount
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apps.users.models import User


@method_decorator(csrf_exempt, name="dispatch")
class SocialLoginView(View):
    def post(self, request, *args, **kwargs):
        access_token = request.POST.get("access_token")

        # Распарсите данные из access token
        url = f"https://oauth2.googleapis.com/tokeninfo?access_token={access_token}"
        response = requests.get(url)
        user_data_token = response.json()

        response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", params={"access_token": access_token})

        user_data = response.json()
        user_data.update(user_data_token)
        print(user_data)

        # Создайте пользователя, если он еще не существует
        users = User.objects.filter(email=user_data["email"])
        if not users:
            user = User.objects.create(
                email=user_data["email"],
            )
            user.set_unusable_password()
            user.save()
        else:
            user = users[0]

        # Залогиньте пользователя
        login(request, user, backend="allauth.account.auth_backends.AuthenticationBackend")

        # Создайте запись в таблице SocialAccount
        social_accounts = SocialAccount.objects.filter(user=user)
        print(social_accounts)

        SocialAccount.objects.create(
            user=user, provider="google", uid=user_data.get("sub", ""), extra_data={**user_data}
        )

        # Создайте запись в таблице EmailAddress
        user_email = EmailAddress.objects.create(
            user=user,
            email=user_data["email"],
            primary=True,
        )
        user_email.verified = True
        user_email.save()

        return HttpResponseRedirect("/")
