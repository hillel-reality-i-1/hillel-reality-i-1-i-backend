# Generated by Django 4.2.7 on 2024-01-29 14:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0021_alter_mention_mentioned_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="comment",
            name="mentions",
        ),
        migrations.RemoveField(
            model_name="post",
            name="mentions",
        ),
        migrations.DeleteModel(
            name="Mention",
        ),
    ]