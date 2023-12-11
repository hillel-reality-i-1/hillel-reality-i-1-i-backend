from django.urls import path
from .views import DeleteUserContentView

from apps.content.api.views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('comments', CommentViewSet, basename='comments')

app_name = 'api-content'

urlpatterns = [
    path("delete-content/", DeleteUserContentView.as_view(), name="delete_user_content"),
]

urlpatterns += router.urls
