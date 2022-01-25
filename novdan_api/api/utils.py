from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from .models import Subscription, SubscriptionTimeRange, Transaction, Wallet


def get_start_of_month(datetime):
    return timezone.datetime(datetime.year, datetime.month, 1, tzinfo=datetime.tzinfo)


def get_end_of_month(datetime):
    return timezone.datetime(datetime.year, datetime.month + 1, 1, tzinfo=datetime.tzinfo) - timezone.timedelta(seconds=1)


def calculate_receivers_percentage(from_wallet):
    now = timezone.now()
    year = now.year
    month = now.month

    transactions = Transaction.objects.filter(
        from_wallet=from_wallet,
        created_at__year=year,
        created_at__month=month,
    )

    sum = transactions.aggregate(Sum('amount')).get('amount__sum', None) or 0
    if sum <= 0:
        return 0, []

    results = transactions.values('to_wallet').order_by('to_wallet').annotate(sum=Sum('amount'))
    percentages = [{ 'id': str(result['to_wallet']), 'percentage': result['sum'] / sum } for result in results]

    return sum, percentages


def generate_tokens_for_month(time=timezone.now()):
    """
    Fills wallets of all users that have a valid subscription with tokens for
    the current month. The amount of tokens in each wallet is set to the number
    of seconds in the current month.
    """
    seconds = int((get_end_of_month(time) - get_start_of_month(time)).total_seconds())

    user_ids_with_subscription = Subscription.objects.current(time).values_list('user_id', flat=True)

    Wallet.objects.filter(user_id__in=user_ids_with_subscription).update(amount=seconds)


def _create_subscription_time_range(time, subscription_id):
    starts_at = get_start_of_month(time)
    ends_at = get_end_of_month(time)

    return SubscriptionTimeRange.objects.create(
        starts_at=starts_at,
        ends_at=ends_at,
        subscription_id=subscription_id,
    )


def generate_subscription_time_ranges_for_month(time=timezone.now()):
    """
    Creates a new SubscriptionTimeRange for the current month for all
    subscriptions where their last time range was not canceled.

    Asserts if any ranges for current month already exist!
    """

    # make sure there are not any time ranges for this month already
    month_has_time_ranges = SubscriptionTimeRange.objects.current(time).exists()
    assert not month_has_time_ranges, "A SubscriptionTimeRange for current month already exists!"

    # get last time range for each subscription
    last_time_ranges = SubscriptionTimeRange.objects.all() \
        .order_by('subscription', '-ends_at') \
        .distinct('subscription')

    # filter non canceled time ranges from last time ranges
    # this needs to happen separately otherwise filter is executed before distinct
    non_canceled_subscription_ids = SubscriptionTimeRange.objects \
        .filter(pk__in=last_time_ranges, canceled_at__isnull=True) \
        .values_list('subscription_id', flat=True)

    for subscription_id in non_canceled_subscription_ids:
        _create_subscription_time_range(time, subscription_id)


def activate_subscription(user, payment_token):
    """
    Activates payed subscription for user.

    Asserts if payment token is none or empty!
    Asserts if subscription is already payed!
    """
    time = timezone.now()

    # make sure payment token is not empty
    assert payment_token is not None and payment_token != '', "Payment token is none or empty!"

    with transaction.atomic():
        subscription, _ = Subscription.objects.get_or_create(user=user)

        # make sure subscription is not already payed
        assert not subscription.is_payed(time), "Subscription is already payed!"

        # try getting current unpayed subscription time range if it exists
        time_range = subscription.time_ranges.current(time).unpayed().first()

        # create new time range if it does not exist
        if not time_range:
            time_range = _create_subscription_time_range(time, subscription.id)

        # add payment data and save
        time_range.payed_at = time
        time_range.payment_token = payment_token
        time_range.save()

        # fill wallet with tokens for this month
        seconds = int((get_end_of_month(time) - get_start_of_month(time)).total_seconds())
        Wallet.objects.filter(user=user).update(amount=seconds)


def cancel_subscription(user):
    """
    Cancels subscription for user.

    Asserts if subscription is not active!
    """
    time = timezone.now()

    with transaction.atomic():
        subscription = Subscription.objects.get(user=user)

        # make sure subscription is payed
        assert subscription.is_payed(time), "Subscription is not payed!"

        # get current payed subscription time range
        time_range = subscription.time_ranges.current(time).payed().first()

        # TODO: cancel payment in podpri api

        # add cancelation data and save
        time_range.canceled_at = time
        time_range.save()
