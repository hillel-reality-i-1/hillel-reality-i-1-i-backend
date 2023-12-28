# Generated by Django 4.2.7 on 2023-12-28 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        ("expert", "0001_initial"),
        ("files", "0002_initial"),
        ("content", "0009_comment_helpful_count_comment_not_helpful_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="country",
            field=models.ManyToManyField(related_name="post_countries", to="cities_light.country"),
        ),
        migrations.RemoveField(
            model_name="post",
            name="images",
        ),
        migrations.AlterField(
            model_name="post",
            name="professional_tags",
            field=models.ManyToManyField(related_name="professional_tags", to="expert.profession"),
        ),
        migrations.AddField(
            model_name="post",
            name="images",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="post_images",
                to="files.image",
            ),
        ),
    ]
