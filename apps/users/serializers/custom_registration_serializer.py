from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegistrationSerializer(RegisterSerializer):

    def save(self, request):
        user = super().save(request)

        user.first_name = "Anonim"

        user.save()
        return user
