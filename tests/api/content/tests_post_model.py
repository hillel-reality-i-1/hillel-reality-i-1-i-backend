from django.urls import reverse
from apps.content.api.views import PostViewSet

POST_LIST_LINK = reverse('api-content:posts-list')
NON_REVERSE_POST_DETAIL_LINK = 'api-content:posts-detail'
LOGIN_LINK = reverse('rest_login')
MAX_POST_ON_PAGE = PostViewSet.pagination_class.max_page_size


def test_create_post(post_data, create_post, post_model, default_user):
    author = default_user
    create_post(author=author, **post_data)
    assert post_model.objects.all().count() == 1


def test_get_post_list(post_data, create_post, default_user, api_client):
    author = default_user
    for _ in range(2*MAX_POST_ON_PAGE):
        create_post(author=author, **post_data)

    page_size = MAX_POST_ON_PAGE
    response = api_client.get(POST_LIST_LINK, data={"page_size": page_size})
    second_page_url = response.json()['next']
    response = api_client.get(second_page_url)

    assert response.status_code == 200
    assert response.json()['next'] is None

    page_size = 2 * MAX_POST_ON_PAGE
    response = api_client.get(POST_LIST_LINK, data={"page_size": page_size})
    second_page_url = response.json()['next']
    response = api_client.get(second_page_url)

    assert response.status_code == 200
    assert response.json()['next'] is None


def test_create_post_login_user(api_client, default_verified_user, post_data, user_data):
    user = default_verified_user
    response = api_client.post(LOGIN_LINK, {
        'password': user_data['password'],
        'email': user_data['email'],
    })
    token = response.json()['key']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = api_client.post(POST_LIST_LINK, data=post_data)

    assert response.status_code == 201
    assert response.json()['author'] == user.username
    assert response.json()['title'] == post_data['title']
    assert response.json()['content'] == post_data['content']


def test_create_post_not_login_user(api_client, default_verified_user, post_data):
    user = default_verified_user
    post_data.update({'author': user.id})
    response = api_client.post(POST_LIST_LINK, data=post_data)

    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}


def test_get_post_by_id(api_client, default_verified_user, post_data, user_data):
    user = default_verified_user
    user.save()
    response = api_client.post(LOGIN_LINK, {
        'password': user_data['password'],
        'email': user_data['email'],
    })
    token = response.json()['key']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    response = api_client.post(POST_LIST_LINK, data=post_data)

    post_dict = response.json()

    post_id = post_dict['id']

    response = api_client.get(
        reverse(NON_REVERSE_POST_DETAIL_LINK, args=[post_id])
    )

    assert response.status_code == 200
    assert response.json() == post_dict
