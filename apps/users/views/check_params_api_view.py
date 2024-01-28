from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.users.models import UserProfile


@api_view(["GET"])
def check_params_api(request):
    username = request.query_params.get("username", None)
    phone_number = request.query_params.get("phone_number", None)
    response = {
        "username_exists": get_user_model().objects.filter(username=username).exists() if username else None,
        "phone_exists": UserProfile.objects.filter(phone_number=phone_number).exists() if phone_number else None,
    }

    return Response(response)
