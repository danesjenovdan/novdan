from django.core.management.base import BaseCommand
from django.utils import timezone

from ...utils import (
    generate_subscription_time_ranges_for_month,
    generate_tokens_for_month,
)


class Command(BaseCommand):
    help = "Generates monthly tokens for all valid wallets."

    def handle(self, *args, **options):
        self.stdout.write("Starting ...")

        self.stdout.write(f"time = {timezone.now()}")

        self.stdout.write("generate_subscription_time_ranges_for_month ...")
        generate_subscription_time_ranges_for_month()

        self.stdout.write("generate_tokens_for_month ...")
        generate_tokens_for_month()

        self.stdout.write("Done")
