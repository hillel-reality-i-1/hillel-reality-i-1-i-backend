# Generated by Django 4.2.7 on 2024-01-16 09:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expert", "0002_category"),
        ("users", "0007_userprofile_email_is_visible_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofileextended",
            name="profession",
        ),
        migrations.RemoveField(
            model_name="userprofileextended",
            name="service",
        ),
        migrations.AddField(
            model_name="userprofileextended",
            name="profession",
            field=models.ManyToManyField(blank=True, null=True, to="expert.profession"),
        ),
        migrations.AddField(
            model_name="userprofileextended",
            name="service",
            field=models.ManyToManyField(blank=True, null=True, to="expert.service"),
        ),
    ]
