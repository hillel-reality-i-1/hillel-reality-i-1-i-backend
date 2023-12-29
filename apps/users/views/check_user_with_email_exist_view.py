from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.users.serializers.check_email_serializer import UserCheckEmailSerializer


class CheckEmailExists(APIView):

    serializer_class = UserCheckEmailSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)

        if not email:
            return Response(
                {'error': 'Будь ласка, введіть електронну адресу.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Перевірка існування користувача з вказаною електронною адресою
        user_exists = get_user_model().objects.filter(email=email).exists()

        if user_exists:
            return Response(
                {
                    'exists': True,
                    'message': 'Користувач із вказаною електронною адресою існує.'
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'exists': False,
                    'message': 'Користувач із вказаною електронною адресою не знайдений.'
                },
                status=status.HTTP_200_OK
            )
