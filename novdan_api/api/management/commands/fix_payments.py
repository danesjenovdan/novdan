from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from ...models import Subscription, Wallet
from ...utils import (
    _get_or_create_subscription_time_range,
    generate_tokens_for_month_for_wallet,
)

PAYMENTS_TO_FIX = [
    (
        "jjnncz",
        "rm335r04",
        "2026-06-07T19:23:11",
    ),
    (
        "jnb6k5",
        "a8gqsp82",
        "2026-06-04T12:07:40",
    ),
    (
        "5vsdv5",
        "b8ngx6rs",
        "2026-06-04T09:18:58",
    ),
    (
        "88d6dk",
        "ddvabch6",
        "2026-06-03T22:33:36",
    ),
    (
        "2qccvq",
        "qw4e2sjt",
        "2026-06-03T19:22:03",
    ),
    (
        "jwy8cf",
        "9hxy2h91",
        "2026-06-02T05:31:29",
    ),
    (
        "9mtvwv",
        "7f4htxqk",
        "2026-06-01T13:23:32",
    ),
    (
        "5f2kkq",
        "7qjfzysv",
        "2026-06-01T13:23:10",
    ),
    (
        "ccpbsz",
        "7f2v3q42",
        "2026-06-01T13:16:23",
    ),
    (
        "2sdvf5",
        "ah8bjk8j",
        "2026-06-01T13:23:32",
    ),
    (
        "jbm8xf",
        "rs57jgwp",
        "2026-06-01T13:23:10",
    ),
    (
        "gm5dfq",
        "29sd8b3c",
        "2026-06-01T13:20:04",
    ),
    (
        "cp9zwv",
        "eqhh3wzc",
        "2026-06-01T13:23:10",
    ),
    (
        "b34svq",
        "px2xf7w8",
        "2026-06-01T13:23:32",
    ),
    (
        "dcv2dk",
        "gdt0tws6",
        "2026-06-01T13:23:32",
    ),
    (
        "jyb3jk",
        "nfdy439e",
        "2026-06-01T13:23:32",
    ),
    (
        "hxwpw9",
        "3y3avxpg",
        "2026-06-01T13:23:32",
    ),
    (
        "7n7fkq",
        "6wc9w2r0",
        "2026-06-01T13:23:32",
    ),
    (
        "9yvkbv",
        "7r7pbcdj",
        "2026-06-01T13:20:04",
    ),
    (
        "hdgt95",
        "rfkd0453",
        "2026-06-01T13:20:04",
    ),
    (
        "6yv7qv",
        "9vzy0vhy",
        "2026-06-01T13:23:32",
    ),
    (
        "fvzbtq",
        "5sqegept",
        "2026-06-01T13:23:10",
    ),
    (
        "jkvhvp",
        "h10mknmg",
        "2026-06-01T12:07:03",
    ),
    (
        "7zqcrz",
        "d8h994n2",
        "2026-06-01T12:07:18",
    ),
    (
        "82tqcz",
        "qp0k847z",
        "2026-05-30T12:04:02",
    ),
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Starting ...")

        for tr in PAYMENTS_TO_FIX:
            subscription_id = tr[0]
            transaction_id = tr[1]
            settled_date = tr[2]

            try:
                subscriptions = Subscription.objects.filter(
                    time_range__payment_token=subscription_id
                ).distinct()
                sub = subscriptions.first()
                print(
                    f"Found {subscriptions.count()} subscriptions for subscription_id {subscription_id}"
                )
                if sub:
                    print(sub)
                    with transaction.atomic():
                        subscription = sub
                        time = timezone.make_aware(
                            datetime.strptime(settled_date, "%Y-%m-%dT%H:%M:%S")
                        )
                        payment_token = subscription_id
                        user = subscription.user

                        # make sure subscription is not already payed
                        if subscription.time_ranges.current(time).payed().exists():
                            self.stdout.write(
                                f"Subscription {subscription_id} is already payed, skipping"
                            )
                            continue

                        # try getting or create new subscription time range
                        time_range = _get_or_create_subscription_time_range(
                            time, subscription.id
                        )

                        # add payment data and save
                        time_range.payed_at = time
                        time_range.payment_token = payment_token
                        time_range.save()

                        # fill wallet with tokens for this month
                        generate_tokens_for_month_for_wallet(
                            Wallet.objects.get(user=user), time
                        )

                        self.stdout.write(
                            f"Fixed payment for subscription {subscription_id} with settled at {settled_date}"
                        )

            except Subscription.DoesNotExist:
                self.stdout.write(f"Subscription {subscription_id} does not exist")

        self.stdout.write("Done")
