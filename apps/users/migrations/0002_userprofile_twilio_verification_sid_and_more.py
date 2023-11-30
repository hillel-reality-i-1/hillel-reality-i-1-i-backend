# Generated by Django 4.2.7 on 2023-11-22 10:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="twilio_verification_sid",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="twilio_verified",
            field=models.BooleanField(default=False),
        ),
    ]