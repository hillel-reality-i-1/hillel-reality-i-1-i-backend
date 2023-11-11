def test_create_comment(comment_data, create_comment, comment_model, default_article):
    article = default_article
    author = article.author
    create_comment(author=author, article=article, **comment_data)
    assert comment_model.objects.all().count() == 1
