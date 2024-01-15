from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.models import UserProfile


class ChangeContactVisibilityView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        contact_type = request.data.get('contact_type')

        if contact_type not in [
            'telegram', 'instagram', 'facebook', 'linkedin', 'phone_number', 'email',
        ]:
            return Response({'error': 'Невірний тип контакту'}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = UserProfile.objects.get(user=request.user)

        result = False

        if contact_type == 'telegram':
            result = not user_profile.telegram_is_visible
            user_profile.telegram_is_visible = result
        elif contact_type == 'instagram':
            result = not user_profile.instagram_is_visible
            user_profile.instagram_is_visible = result
        elif contact_type == 'facebook':
            result = not user_profile.facebook_is_visible
            user_profile.facebook_is_visible = result
        elif contact_type == 'linkedin':
            result = not user_profile.linkedin_is_visible
            user_profile.linkedin_is_visible = result
        elif contact_type == 'phone_number':
            result = not user_profile.phone_is_visible
            user_profile.phone_is_visible = result
        elif contact_type == 'email':
            result = not user_profile.email_is_visible
            user_profile.email_is_visible = result

        user_profile.save()

        return Response({"details": f"Visibility of {contact_type} set to {result}"}, status=status.HTTP_200_OK)