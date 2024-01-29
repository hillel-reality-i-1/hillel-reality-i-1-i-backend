# Generated by Django 4.2.7 on 2024-01-29 10:00

import apps.files.models.image
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("files", "0002_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PostImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "post_image",
                    models.ImageField(null=True, upload_to=apps.files.models.image.universal_file_path_builder),
                ),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
