from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.files.api.views.get_image_by_user_id_view import ImageByUserIdView
from apps.files.api.views.image_list_view import ImageListView
from apps.files.api.views.portfolio_list_view import PortfolioListView
from apps.files.api.views.post_image_delete_view import PostImageDeleteView

router = DefaultRouter()
router.register(r"img_list", ImageListView, basename="img_list")
router.register(r"portfolio_list", PortfolioListView, basename="portfolio_list")


urlpatterns = [
    path("", include(router.urls)),
    path("images_by_user_id/<int:user_id>/", ImageByUserIdView.as_view(), name="images_by_user_id"),
    path("post_image/<int:pk>/delete", PostImageDeleteView.as_view(), name="post_image_delete"),
]
