# Generated by Django 4.2.7 on 2023-12-18 18:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0008_alter_post_country_alter_post_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="worldwide",
            field=models.BooleanField(default=False),
        ),
    ]