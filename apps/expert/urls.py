from django.urls import path

from .views.service_view import ServiceListView, ServiceCreateView
from .views.profession_view import ProfessionListView, ProfessionCreateView

urlpatterns = [
    path("professions/", ProfessionListView.as_view(), name="all_professions"),
    path("professions/create", ProfessionCreateView.as_view(), name="create_profession"),
    #
    path("services/", ServiceListView.as_view(), name="all_services"),
    path("services/create", ServiceCreateView.as_view(), name="create_service"),
    #
]
