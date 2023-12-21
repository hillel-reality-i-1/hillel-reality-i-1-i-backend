# Generated by Django 4.2.7 on 2023-12-18 08:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0005_alter_post_images"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="dislikes",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="images",
        ),
        migrations.RemoveField(
            model_name="comment",
            name="likes",
        ),
        migrations.AddField(
            model_name="post",
            name="reactions",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]