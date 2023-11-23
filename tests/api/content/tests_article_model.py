from django.urls import reverse
from apps.content.api.views import ArticleViewSet

ARTICLE_LIST_LINK = reverse('api-content:articles-list')
NON_REVERSE_ARTICLE_DETAIL_LINK = 'api-content:articles-detail'
LOGIN_LINK = reverse('rest_login')
MAX_ARTICLE_ON_PAGE = ArticleViewSet.pagination_class.max_page_size


def test_create_article(article_data, create_article, article_model, default_user):
    author = default_user
    create_article(author=author, **article_data)
    assert article_model.objects.all().count() == 1


def test_get_articles_list(article_data, create_article, default_user, api_client):
    author = default_user
    for _ in range(2*MAX_ARTICLE_ON_PAGE):
        create_article(author=author, **article_data)

    page_size = MAX_ARTICLE_ON_PAGE
    response = api_client.get(ARTICLE_LIST_LINK, data={"page_size": page_size})
    second_page_url = response.json()['next']
    response = api_client.get(second_page_url)

    assert response.json()['next'] is None

    page_size = 2 * MAX_ARTICLE_ON_PAGE
    response = api_client.get(ARTICLE_LIST_LINK, data={"page_size": page_size})
    second_page_url = response.json()['next']
    response = api_client.get(second_page_url)

    assert response.json()['next'] is None

    page_size = MAX_ARTICLE_ON_PAGE
    create_article(author=author, **article_data)
    response = api_client.get(ARTICLE_LIST_LINK, data={"page_size": page_size})
    second_page_response = api_client.get(response.json()['next'])
    third_page_response = api_client.get(second_page_response.json()['next'])

    assert len(third_page_response.json()['results']) == 1


def test_create_article_login_user(api_client, default_verified_user, article_data, user_data):
    user = default_verified_user
    response = api_client.post(LOGIN_LINK, {
        'password': user_data['password'],
        'email': user_data['email'],
    })
    token = response.json()['key']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = api_client.post(ARTICLE_LIST_LINK, data=article_data)

    assert response.status_code == 201
    assert response.json()['author'] == user.username
    assert response.json()['title'] == article_data['title']
    assert response.json()['content'] == article_data['content']


def test_create_article_not_login_user(api_client, default_verified_user, article_data):
    user = default_verified_user
    article_data.update({'author': user.id})
    response = api_client.post(ARTICLE_LIST_LINK, data=article_data)

    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}
