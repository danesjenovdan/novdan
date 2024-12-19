from django.core.management.base import BaseCommand, CommandError

from ...models import Subscription
from ...utils import get_end_of_month, get_start_of_month


class Command(BaseCommand):
    help = "Validate that all time ranges are correctly set."

    def handle(self, *args, **options):
        self.stdout.write("Starting ...")

        problematic_time_ranges = set()

        for subscription in Subscription.objects.all():
            seen_months = set()

            for time_range in subscription.time_ranges.all():
                self.stdout.write(
                    f"SubscriptionTimeRange: user={subscription.user} id={time_range.id}"
                )

                if (
                    time_range.starts_at.month != time_range.ends_at.month
                    or time_range.starts_at.year != time_range.ends_at.year
                ):
                    self.stdout.write(" - start and end are different months")
                    problematic_time_ranges.add(time_range.id)

                if time_range.starts_at != get_start_of_month(time_range.starts_at):
                    self.stdout.write(" - start is not start of month")
                    problematic_time_ranges.add(time_range.id)

                if time_range.ends_at != get_end_of_month(time_range.starts_at):
                    self.stdout.write(" - end is not end of month")
                    problematic_time_ranges.add(time_range.id)

                year_month_string = (
                    f"{time_range.starts_at.year}-{time_range.starts_at.month}"
                )
                if year_month_string in seen_months:
                    self.stdout.write(f" - duplicate month {year_month_string}")
                    problematic_time_ranges.add(time_range.id)

                seen_months.add(year_month_string)

        if len(problematic_time_ranges):
            raise CommandError(
                f"Problems with {len(problematic_time_ranges)} time range(s)!"
            )

        self.stdout.write(self.style.SUCCESS("Done"))
