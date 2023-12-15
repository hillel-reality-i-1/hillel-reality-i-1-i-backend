from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.files.api.views.image_list_view import ImageListView
from apps.files.api.views.portfolio_list_view import PortfolioListView

router = DefaultRouter()
router.register(r"img_list", ImageListView, basename="img_list")
router.register(r"portfolio_list", PortfolioListView, basename="portfolio_list")


urlpatterns = [
    path("", include(router.urls)),
]
