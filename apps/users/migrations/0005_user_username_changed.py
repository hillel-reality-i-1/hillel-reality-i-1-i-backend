# Generated by Django 4.2.7 on 2023-12-20 12:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_remove_user_first_name_remove_user_last_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="username_changed",
            field=models.BooleanField(default=False),
        ),
    ]