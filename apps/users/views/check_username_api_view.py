from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def check_username_api(request):
    username = request.query_params.get("username", None)
    if username is None:
        return Response({"error": "Bad Request. 'username' parameter is required."}, status=400)
    username_exists = get_user_model().objects.filter(username=username).exists()

    return Response({"username_exists": username_exists})
