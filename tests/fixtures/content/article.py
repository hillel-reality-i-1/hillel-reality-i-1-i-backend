import pytest
from apps.content.models import Article
from ..user.user import get_default_user


def _create_article(author, content, title):
    return Article.objects.create(author=author, content=content, title=title)


def _article_data():
    return {
        'content': 'content',
        'title': 'title',
    }


def get_default_article():
    user = get_default_user()
    article = _create_article(author=user, **_article_data())
    return article


@pytest.fixture
def article_data():
    return _article_data()


@pytest.fixture
def create_article():
    return _create_article


@pytest.fixture
def article_model():
    return Article


@pytest.fixture
def default_article():
    return get_default_article()
