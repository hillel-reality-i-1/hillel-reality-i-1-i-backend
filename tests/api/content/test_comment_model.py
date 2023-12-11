def test_create_comment(comment_data, create_comment, comment_model, default_post):
    post = default_post
    author = post.author
    create_comment(author=author, post=post, **comment_data)
    assert comment_model.objects.all().count() == 1
