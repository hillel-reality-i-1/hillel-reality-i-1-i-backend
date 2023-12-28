from django.urls import path

from .views import DeleteUserContentView
from apps.content.api.views.posts.post_reactions_create_view import PostReactionCreateView
from .views.comments.vote_helpful_view import VoteHelpfulView, VoteNotHelpfulView
from .views.contributions.contribution_list_view import ContributionListView
from .views.contributions.vote_contribution_view import VoteContributionView
from .views.posts import PostListView, PostCreateView, PostModifiedDeleteView
from .views.comments import CommentModifiedDeleteView, NestedCommentsCreateView, CommentsCreateView, CommentsListView

app_name = "api-content"

urlpatterns = [
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostModifiedDeleteView.as_view(), name="post-detail"),
    path("post/<int:post_id>/reactions/create/", PostReactionCreateView.as_view(), name="post-reaction-create"),
    path("post/<int:pk>/comment/create", CommentsCreateView.as_view(), name="comment-create"),
    path("post/<int:pk>/comments/", CommentsListView.as_view(), name="comment-list"),
    path("comment/<int:pk>/", CommentModifiedDeleteView.as_view(), name="comment-modified-del"),
    path("comment/<int:pk>/replies/", NestedCommentsCreateView.as_view(), name="nested-comment-create"),
    path("comment/<int:comment_id>/vote_helpful/", VoteHelpfulView.as_view(), name="vote_helpful"),
    path("comment/<int:comment_id>/vote_not_helpful/", VoteNotHelpfulView.as_view(), name="vote_not_helpful"),
    path("post/<int:pk>/contributions/", ContributionListView.as_view(), name="contribution_list"),
    path("contribution/<int:pk>/vote_helpful/", VoteContributionView.as_view(), name="vote_contribution_helpful"),
    path("delete-content/", DeleteUserContentView.as_view(), name="delete_user_content"),
]
