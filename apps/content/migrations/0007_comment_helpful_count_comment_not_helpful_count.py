# Generated by Django 4.2.7 on 2023-12-27 18:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0006_remove_contribution_dislikes_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="helpful_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="comment",
            name="not_helpful_count",
            field=models.IntegerField(default=0),
        ),
    ]