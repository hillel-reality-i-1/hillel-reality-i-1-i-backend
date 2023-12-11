from cities_light.models import Country, City
from django.db import models
from apps.files.models import Image
from apps.users.models import User
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(max_length=15, null=True, blank=True)
    about_my_self = models.TextField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    phone_verified = models.BooleanField(default=False)

    # Fields for Twilio verification
    twilio_verification_sid = models.CharField(max_length=255, null=True, blank=True)

    # Fields for Vonage(nexmo) verification
    phone_verified_request_id = models.CharField(max_length=255, null=True, blank=True)

    def change_phone_number(self, new_phone_number):
        # Изменяем номер телефона и сбрасываем статус верификации
        self.phone_number = new_phone_number
        self.phone_verified = False  # Добавьте эту строку для сброса статуса верификации
        self.twilio_verification_sid = None  # Сбрасываем данные для Twilio, так как номер изменен
        self.phone_verified_request_id = None  # Сбрасываем данные для Vonage (nexmo), так как номер изменен
        self.save()

    def __str__(self):
        return f"{self.user.username}'s user profile"
