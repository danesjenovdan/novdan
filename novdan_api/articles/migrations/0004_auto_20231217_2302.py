# Generated by Django 3.2.8 on 2023-12-17 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0003_article"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="image_url",
            field=models.URLField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name="article",
            name="url",
            field=models.URLField(max_length=512),
        ),
    ]
