# Generated by Django 4.2.7 on 2024-02-06 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonenumbers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumber',
            name='verification_code_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]