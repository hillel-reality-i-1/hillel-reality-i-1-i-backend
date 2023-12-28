from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils.translation import activate


@api_view(["GET"])
def set_language_api(request, language_code):
    language_code = "en" if language_code != "uk" else "uk"

    # Включаем выбранный язык
    activate(language_code)

    # Опционально: Записываем язык в сессию, чтобы хранить его между запросами
    request.session["django_language"] = language_code
    request.session.save()

    # Возвращаем JSON-ответ
    return Response({"success": True})
