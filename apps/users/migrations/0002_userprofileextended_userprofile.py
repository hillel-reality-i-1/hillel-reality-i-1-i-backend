# Generated by Django 4.2.7 on 2023-11-09 09:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("files", "0001_initial"),
        ("expert", "0002_rename_title_profession_name_and_more"),
        ("cities_light", "0011_alter_city_country_alter_city_region_and_more"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfileExtended",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("about_my_self_ext", models.TextField(blank=True, null=True)),
                ("profession", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="expert.profession")),
                ("resume", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="files.file")),
                ("service", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="expert.service")),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
                ),
                ("about_my_self", models.TextField(blank=True, null=True)),
                (
                    "city",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="cities_light.city"
                    ),
                ),
                ("country", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="cities_light.country")),
                (
                    "profile_picture",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="files.image"),
                ),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
    ]