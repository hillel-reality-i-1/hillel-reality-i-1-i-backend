from django.urls import path

from apps.content.api.views.posts.post_reactions_create_remove_view import PostReactionCreateRemoveView
from .views.comments.vote_helpful_view import VoteHelpfulView, VoteNotHelpfulView
from .views.contribution_view import ContributionListView
from .views.posts import (
    PostListView,
    PostCreateView,
    PostModifiedView,
    PostDeleteView,
    SaveRemovePostAPIView,
)
from .views.comments import (
    NestedCommentsCreateView,
    CommentsCreateView,
    CommentsListView,
    CommentModifiedView,
    CommentDeleteView,
)
from .views.posts.search_view import SearchView


app_name = "api-content"

urlpatterns = [
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostModifiedView.as_view(), name="post-modified"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="post-delete"),
    path("post/<int:pk>/save-remove/", SaveRemovePostAPIView.as_view(), name="save-remove-post"),
    path("post/<int:post_id>/reactions/create/", PostReactionCreateRemoveView.as_view(), name="post-reaction-create"),
    path("post/<int:pk>/comment/create", CommentsCreateView.as_view(), name="comment-create"),
    path("post/<int:pk>/comments/", CommentsListView.as_view(), name="comment-list"),
    path("comment/<int:pk>/", CommentModifiedView.as_view(), name="comment-modified"),
    path("comment/<int:pk>/delete", CommentDeleteView.as_view(), name="comment-delete"),
    path("comment/<int:pk>/replies/", NestedCommentsCreateView.as_view(), name="nested-comment-create"),
    path("comment/<int:comment_id>/vote_helpful/", VoteHelpfulView.as_view(), name="vote_helpful"),
    path("comment/<int:comment_id>/vote_not_helpful/", VoteNotHelpfulView.as_view(), name="vote_not_helpful"),
    path("post/<int:post_id>/contributions/", ContributionListView.as_view(), name="contributions-list"),
    path("search/", SearchView.as_view(), name="search_view"),
]
