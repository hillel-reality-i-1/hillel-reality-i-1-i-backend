def test_create_user(user_data, create_user, user_model):
    create_user(**user_data)
    assert user_model.objects.all().count() == 1
