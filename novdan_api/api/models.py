import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=True)
    customer_id = models.CharField(max_length=64, blank=True, null=True)


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
    def current(self, time=None):
        if time is None:
            time = timezone.now()

        return self.filter(
            time_range__starts_at__lte=time,
            time_range__ends_at__gte=time,
        )

    def payed(self):
        return self.filter(time_range__payed_at__isnull=False)

    def canceled(self):
        # get last time range for each subscription
        last_time_ranges = SubscriptionTimeRange.objects.filter(subscription__in=self) \
            .order_by('subscription', '-ends_at') \
            .distinct('subscription')

        # filter canceled time ranges from last time ranges
        # this needs to happen separately otherwise filter is executed before distinct
        canceled_subscription_ids = SubscriptionTimeRange.objects \
            .filter(pk__in=last_time_ranges, canceled_at__isnull=False) \
            .values_list('subscription_id', flat=True)

        return self.model.objects.filter(pk__in=canceled_subscription_ids)


class Subscription(models.Model):
    objects = SubscriptionQuerySet.as_manager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Subscription ({self.id})'


class SubscriptionTimeRangeQuerySet(models.QuerySet):
    def current(self, time=None):
        if time is None:
            time = timezone.now()

        return self.filter(starts_at__lte=time, ends_at__gte=time)

    def payed(self):
        return self.filter(payed_at__isnull=False)

    def not_payed(self):
        return self.filter(payed_at__isnull=True)

    def canceled(self):
        return self.filter(canceled_at__isnull=False)

    def not_canceled(self):
        return self.filter(canceled_at__isnull=True)


class SubscriptionTimeRange(models.Model):
    objects = SubscriptionTimeRangeQuerySet.as_manager()

    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    canceled_at = models.DateTimeField(blank=True, null=True)
    payed_at = models.DateTimeField(blank=True, null=True)
    payment_token = models.CharField(max_length=128, blank=True, null=True)
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='time_ranges',
        related_query_name='time_range',
    )


class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField()
    from_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='outgoing_transactions',
        related_query_name='outgoing_transaction',
    )
    to_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name='incoming_transactions',
        related_query_name='incoming_transaction',
    )
