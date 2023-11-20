def test_create_article(article_data, create_article, article_model, default_user):
    author = default_user
    create_article(author=author, **article_data)
    assert article_model.objects.all().count() == 1
