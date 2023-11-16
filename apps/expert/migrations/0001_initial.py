# Generated by Django 4.2.7 on 2023-11-16 08:46

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=100, unique=True, verbose_name="name")),
                ("approved", models.BooleanField(default=False, verbose_name="approved")),
            ],
        ),
        migrations.CreateModel(
            name="Profession",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=100, unique=True, verbose_name="name")),
                ("approved", models.BooleanField(default=False, verbose_name="approved")),
                ("services", models.ManyToManyField(related_name="professions", to="expert.service")),
            ],
        ),
    ]
