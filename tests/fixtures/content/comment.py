import pytest
from apps.content.models import Comment
from .post import get_default_post


def _create_comment(author, post, text):
    return Comment.objects.create(author=author, post=post, text=text)


def _comment_data():
    return {
        'text': 'text',
    }


def get_default_comment():
    post = get_default_post()
    author = post.author
    return _create_comment(author=author, post=post, **_comment_data())


@pytest.fixture
def comment_data():
    return _comment_data()


@pytest.fixture
def create_comment():
    return _create_comment


@pytest.fixture
def comment_model():
    return Comment


@pytest.fixture
def default_comment():
    return get_default_comment()
