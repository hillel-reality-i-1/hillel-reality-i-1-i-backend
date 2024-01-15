# Generated by Django 4.2.7 on 2024-01-15 10:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_userprofileextended_profession_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                default="anonim_user_1",
                max_length=32,
                unique=True,
                validators=[
                    django.core.validators.MinLengthValidator(limit_value=2),
                    django.core.validators.MaxLengthValidator(limit_value=32),
                ],
            ),
        ),
    ]