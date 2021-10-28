import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils import timezone


class User(AbstractUser):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=True)


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.BigIntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Wallet ({self.id})'


class SubscriptionQuerySet(models.QuerySet):
    def active(self):
        return self.filter(
            Q(active_range__started_at__lte=timezone.now()),
            Q(active_range__ended_at__gte=timezone.now()) | Q(active_range__ended_at__isnull=True),
        )


class SubscriptionManager(models.Manager):
    def get_queryset(self):
        return SubscriptionQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()


class Subscription(models.Model):
    objects = SubscriptionManager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    @property
    def is_active(self):
        return self.active_ranges.filter(
            Q(started_at__lte=timezone.now()),
            Q(ended_at__gte=timezone.now()) | Q(ended_at__isnull=True),
        ).exists()

    def __str__(self):
        return f'Subscription ({self.id})'


class SubscriptionTimeRange(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name="active_ranges",
        related_query_name="active_range",
    )
    # TODO: add some kind of payment id from "podpri" api


class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField()
    from_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="outgoing_transactions",
        related_query_name="outgoing_transaction",
    )
    to_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="incoming_transactions",
        related_query_name="incoming_transaction",
    )
