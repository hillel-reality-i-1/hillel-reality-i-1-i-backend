# Generated by Django 4.2.7 on 2024-01-16 11:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0014_merge_20240108_0851"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="professional_tags",
        ),
    ]
