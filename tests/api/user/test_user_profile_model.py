def test_create_user(user_profile_data, create_user_profile, user_profile_model, default_user):
    user = default_user
    create_user_profile(user=user, **user_profile_data)
    assert user_profile_model.objects.all().count() == 1
