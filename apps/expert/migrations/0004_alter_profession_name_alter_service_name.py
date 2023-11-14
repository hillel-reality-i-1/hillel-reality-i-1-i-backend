# Generated by Django 4.2.7 on 2023-11-12 14:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expert", "0003_profession_approved_service_approved_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profession",
            name="name",
            field=models.CharField(max_length=100, unique=True, verbose_name="name"),
        ),
        migrations.AlterField(
            model_name="service",
            name="name",
            field=models.CharField(blank=True, max_length=100, verbose_name="name"),
        ),
    ]
