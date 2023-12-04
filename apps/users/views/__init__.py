from allauth.account.models import EmailAddress
from allauth.socialaccount.signals import pre_social_login
from django.contrib.auth import get_user_model
from django.dispatch import receiver


@receiver(pre_social_login)
def link_to_local_account(sender, request, sociallogin, **kwargs):
    # Check if email is already registered
    email = sociallogin.account.extra_data['email']
    users = get_user_model().objects.filter(email=email)

    if users.exists():
        # Connect this social login to the existing account
        sociallogin.connect(request, users[0])

        # Confirm the email address
        email_address = EmailAddress.objects.filter(email=email).first()
        email_address.verified = True
        email_address.save()
