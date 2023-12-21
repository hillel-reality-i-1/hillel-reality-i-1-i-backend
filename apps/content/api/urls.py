from django.urls import path

from .views import DeleteUserContentView
from apps.content.api.views.posts.post_reactions_create_view import PostReactionCreateView
from .views.posts import PostListView, PostCreateView, PostModifiedDeleteView
from .views.comments import CommentModifiedDeleteView, NestedCommentsCreateView, CommentsCreateView, CommentsListView

app_name = "api-content"

urlpatterns = [
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/<int:pk>/", PostModifiedDeleteView.as_view(), name="post-detail"),
    path("posts/<int:post_id>/reactions/create/", PostReactionCreateView.as_view(), name="post-reaction-create"),
    path("posts/<int:pk>/comments/create", CommentsCreateView.as_view(), name="comment-create"),
    path("posts/<int:pk>/comments/", CommentsListView.as_view(), name="comment-list"),
    path("comments/<int:pk>/", CommentModifiedDeleteView.as_view(), name="comment-modified-del"),
    path("comments/<int:pk>/replies/", NestedCommentsCreateView.as_view(), name="nested-comment-create"),
    path("delete-content/", DeleteUserContentView.as_view(), name="delete_user_content"),
]
