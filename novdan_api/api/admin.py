from datetime import datetime

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateTimeRangeFilter

from .models import Subscription, SubscriptionTimeRange, Transaction, User, Wallet
from .serializers import UserSerializer
from .utils import (
    USER_PAYMENT_AMOUNT,
    VALID_PAYOUT_USERNAMES,
    calculate_receivers_percentage,
    get_start_of_month,
    get_start_of_next_month,
)


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("url", "customer_id")}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("url",)}),)
    search_fields = UserAdmin.search_fields + ("customer_id",)


admin.site.register(User, CustomUserAdmin)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount")
    list_filter = ("user__is_staff",)
    search_fields = ("id", "user__username")


class IsSubscriptionPayedFilter(admin.SimpleListFilter):
    title = "is payed"
    parameter_name = "is_payed"

    def lookups(self, request, model_admin):
        return (
            ("1", _("Yes")),
            ("0", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.payed()
        if self.value() == "0":
            return queryset.exclude(id__in=queryset.payed())
        return queryset


class IsSubscriptionCanceledFilter(admin.SimpleListFilter):
    title = "is canceled"
    parameter_name = "is_canceled"

    def lookups(self, request, model_admin):
        return (
            ("1", _("Yes")),
            ("0", _("No")),
        )

    def queryset(self, request, queryset):
        if self.value() == "1":
            return queryset.canceled()
        if self.value() == "0":
            return queryset.exclude(id__in=queryset.canceled())
        return queryset


class SubscriptionTimeRangeStackedInline(admin.StackedInline):
    model = SubscriptionTimeRange
    fields = (
        "created_at",
        "starts_at",
        "ends_at",
        "canceled_at",
        "payed_at",
        "payment_token",
    )
    readonly_fields = ("created_at",)
    extra = 0
    ordering = ("-ends_at",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_payed", "is_canceled")
    list_filter = (
        "user__is_staff",
        IsSubscriptionPayedFilter,
        IsSubscriptionCanceledFilter,
    )
    search_fields = (
        "id",
        "user__username",
        "user__customer_id",
        "time_range__payment_token",
    )
    inlines = [SubscriptionTimeRangeStackedInline]

    def is_payed(self, obj):
        return obj.time_ranges.current().payed().exists()

    def is_canceled(self, obj):
        last_time_range = obj.time_ranges.order_by("-ends_at").first()
        if last_time_range:
            return last_time_range.canceled_at is not None
        return False


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "from_wallet", "to_wallet", "amount")
    list_filter = (("created_at", DateTimeRangeFilter),)
    search_fields = ("from_wallet__id", "to_wallet__id", "amount")
    readonly_fields = ("created_at",)
    fields = ("created_at", "from_wallet", "to_wallet", "amount")

    def get_urls(self):
        return [
            path("calculate_monthly_split/", self.calculate_monthly_split),
        ] + super().get_urls()

    def calculate_monthly_split(self, request):
        date_string = request.GET.get("date")
        time = timezone.now()
        if date_string:
            time = timezone.make_aware(datetime.strptime(date_string, "%Y-%m-%d"))

        # calculate simple global tokens received percentages --------------------------------------
        sum_, percentages = calculate_receivers_percentage(None, time)

        context_split = {
            "sum": sum_,
            "percentages": sorted(percentages, key=lambda x: x["amount"], reverse=True),
        }
        # ------------------------------------------------------------------------------------------

        # calculate payout split percentages for whole `time.month`
        # however only for valid payments: from start of `time.month + 1` until 2nd day of `time.month + 1` at 23:59
        payment_time_end = (
            get_start_of_next_month(time)
            + timezone.timedelta(days=2)
            - timezone.timedelta(seconds=1)
        )

        # if we are still waiting for all payments to come through, just return the cutoff date
        if timezone.now() < payment_time_end:
            context_payout = {
                "payment_time_end": payment_time_end,
            }

        # if we are past the cutoff date for payments, calculate payouts
        else:
            # initialize an object to store total payout amounts for valid payout users
            total_payout_amounts = {
                username: {
                    "user": UserSerializer(User.objects.get(username=username)).data,
                    "amount": 0,
                }
                for username in VALID_PAYOUT_USERNAMES
            }

            # TODO replace payed with paid everywhere
            payed_subscriptions = Subscription.objects.payed(payment_time_end).distinct(
                "id"
            )

            subscription_count = 0

            for subscription in payed_subscriptions:
                # skip payments after cutoff date
                time_range = (
                    subscription.time_ranges.current(payment_time_end).payed().first()
                )
                if time_range and time_range.payed_at > payment_time_end:
                    continue

                subscription_count += 1

                wallet = Wallet.objects.get(user=subscription.user)
                sub_sum, sub_percentages = calculate_receivers_percentage(wallet, time)

                # if user spent no tokens split evenly between all
                if sub_sum == 0:
                    for username in VALID_PAYOUT_USERNAMES:
                        amount = USER_PAYMENT_AMOUNT / len(VALID_PAYOUT_USERNAMES)

                        total_payout_amounts[username]["amount"] += amount

                # otherwise split by usage
                else:
                    for percentage in sub_percentages:
                        username = percentage["user"]["username"]
                        assert (
                            username in VALID_PAYOUT_USERNAMES
                        ), f"Tried to pay out to user '{username}' but they are not included in valid payout usernames!"

                        amount = USER_PAYMENT_AMOUNT * percentage["percentage"]

                        total_payout_amounts[username]["amount"] += amount

            context_payout = {
                "payout_amounts": sorted(
                    list(total_payout_amounts.values()),
                    key=lambda x: x["amount"],
                    reverse=True,
                ),
                "payout_sum": sum(
                    map(lambda x: x["amount"], list(total_payout_amounts.values()))
                ),
                "payment_count": subscription_count,
                "payment_amount": USER_PAYMENT_AMOUNT,
                "payment_sum": subscription_count * USER_PAYMENT_AMOUNT,
            }

        # ------------------------------------------------------------------------------------------

        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            # Anything else you want in the context...
            split=context_split,
            payout=context_payout,
            time=time,
        )

        return TemplateResponse(
            request,
            "admin/api/transaction/calculate_monthly_split.html",
            context,
        )
