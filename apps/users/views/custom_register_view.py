from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny

from apps.users.serializers.custom_register_serializer import CustomUserSerializer


class CustomRegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {"username": user.username, "token": token.key, "id": user.id, "email": user.email},
            status=status.HTTP_201_CREATED,
        )
