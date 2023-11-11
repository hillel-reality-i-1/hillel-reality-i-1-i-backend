import pytest
from apps.content.models import Comment
from .article import get_default_article


def _create_comment(author, article, text):
    return Comment.objects.create(author=author, article=article, text=text)


def _comment_data():
    return {
        'text': 'text',
    }


def get_default_comment():
    article = get_default_article()
    author = article.author
    return _create_comment(author=author, article=article, **_comment_data())


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
