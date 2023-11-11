from apps.content.api.views import ArticleViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='articles')
router.register('comments', CommentViewSet, basename='comments')

app_name = 'api-content'

urlpatterns = []

urlpatterns += router.urls
