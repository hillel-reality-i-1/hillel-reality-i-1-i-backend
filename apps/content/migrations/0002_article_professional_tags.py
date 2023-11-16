# Generated by Django 4.2.7 on 2023-11-10 14:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expert", "0003_profession_approved_service_approved_and_more"),
        ("content", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="professional_tags",
            field=models.ManyToManyField(blank=True, related_name="professional_tags", to="expert.profession"),
        ),
    ]