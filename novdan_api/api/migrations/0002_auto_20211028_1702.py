# Generated by Django 3.2.8 on 2021-10-28 17:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="subscriptiontimerange",
            name="ended_at",
        ),
        migrations.RemoveField(
            model_name="subscriptiontimerange",
            name="started_at",
        ),
        migrations.AddField(
            model_name="subscriptiontimerange",
            name="canceled_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="subscriptiontimerange",
            name="ends_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="subscriptiontimerange",
            name="payed_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="subscriptiontimerange",
            name="payment_id",
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="subscriptiontimerange",
            name="starts_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
