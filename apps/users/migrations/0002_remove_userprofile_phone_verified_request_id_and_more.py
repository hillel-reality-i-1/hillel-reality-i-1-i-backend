# Generated by Django 4.2.7 on 2024-01-04 11:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0012_alter_contributionvote_unique_together_and_more"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="phone_verified_request_id",
        ),
        migrations.AddField(
            model_name="userprofile",
            name="saved_comments",
            field=models.ManyToManyField(blank=True, related_name="saved_comments_by_users", to="content.comment"),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="saved_posts",
            field=models.ManyToManyField(blank=True, related_name="saved_posts_by_users", to="content.post"),
        ),
    ]