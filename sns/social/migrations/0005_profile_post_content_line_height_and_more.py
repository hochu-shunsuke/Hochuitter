# Generated by Django 5.1.5 on 2025-02-11 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social", "0004_profile_icon_picture"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="post_content_line_height",
            field=models.FloatField(default=1.4),
        ),
        migrations.AddField(
            model_name="profile",
            name="post_vertical_padding",
            field=models.FloatField(default=0.75),
        ),
    ]
