# Generated by Django 4.2.7 on 2023-12-18 18:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("files", "0002_initial"),
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        ("content", "0006_remove_comment_dislikes_remove_comment_images_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(max_length=10000, validators=[django.core.validators.MinValueValidator(100)]),
        ),
        migrations.RemoveField(
            model_name="post",
            name="country",
        ),
        migrations.AlterField(
            model_name="post",
            name="images",
            field=models.ManyToManyField(blank=True, null=True, related_name="post_images", to="files.image"),
        ),
        migrations.AlterField(
            model_name="post",
            name="title",
            field=models.CharField(max_length=100, validators=[django.core.validators.MinValueValidator(2)]),
        ),
        migrations.AddField(
            model_name="post",
            name="country",
            field=models.ManyToManyField(null=True, related_name="post_countries", to="cities_light.country"),
        ),
    ]
