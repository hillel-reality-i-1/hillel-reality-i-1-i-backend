# Generated by Django 4.2.7 on 2024-01-29 11:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0019_alter_post_post_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="post_image",
        ),
    ]
