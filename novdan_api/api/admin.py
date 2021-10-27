from django.contrib import admin
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Wallet, Subscription, SubscriptionTimeRange, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount')
    list_filter = ('user__is_staff',)
    search_fields = ('id', 'user__username')


class IsSubscriptionActiveFilter(admin.SimpleListFilter):
    title = 'is active'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Yes')),
            ('0', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(
                Q(active_range__started_at__lte=timezone.now()),
                Q(active_range__ended_at__gte=timezone.now()) | Q(active_range__ended_at__isnull=True),
            )
        if self.value() == '0':
            return queryset.exclude(
                Q(active_range__started_at__lte=timezone.now()),
                Q(active_range__ended_at__gte=timezone.now()) | Q(active_range__ended_at__isnull=True),
            )
        return queryset


class SubscriptionTimeRangeStackedInline(admin.StackedInline):
    model = SubscriptionTimeRange
    readonly_fields = ('started_at',)
    fields = ('started_at', 'ended_at')
    extra = 0


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_active')
    list_filter = ('user__is_staff', IsSubscriptionActiveFilter)
    search_fields = ('id', 'user__username')
    inlines = [SubscriptionTimeRangeStackedInline]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
