# Generated by Django 3.2.8 on 2022-01-25 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_auto_20220117_1417"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="customer_id",
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
