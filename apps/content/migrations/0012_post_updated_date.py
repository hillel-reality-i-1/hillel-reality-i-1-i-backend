# Generated by Django 4.2.7 on 2023-12-20 10:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("content", "0011_comment_parent_comment_updated_date_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="updated_date",
            field=models.DateTimeField(auto_now=True),
        ),
    ]