# Generated by Django 4.2.7 on 2023-11-22 11:38

import apps.files.models.image
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("files", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.ImageField(upload_to=apps.files.models.image.universal_file_path_builder),
        ),
    ]