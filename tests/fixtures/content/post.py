import pytest
from apps.content.models import Post
from ..user.user import get_default_user


def _create_post(author, content, title):
    return Post.objects.create(author=author, content=content, title=title)


def _post_data():
    return {
        'content': 'content',
        'title': 'title',
    }


def get_default_post():
    user = get_default_user()
    post = _create_post(author=user, **_post_data())
    return post


@pytest.fixture
def post_data():
    return _post_data()


@pytest.fixture
def create_post():
    return _create_post


@pytest.fixture
def post_model():
    return Post


@pytest.fixture
def default_post():
    return get_default_post()
