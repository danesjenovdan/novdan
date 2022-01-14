from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateTimeRangeFilter

from .models import User, Wallet, Subscription, SubscriptionTimeRange, Transaction


admin.site.register(User, UserAdmin)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount')
    list_filter = ('user__is_staff',)
    search_fields = ('id', 'user__username')


class IsSubscriptionPayedFilter(admin.SimpleListFilter):
    title = 'is payed'
    parameter_name = 'is_payed'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Yes')),
            ('0', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.active().payed()
        if self.value() == '0':
            return queryset.exclude(id__in=queryset.active().payed())
        return queryset


class SubscriptionTimeRangeStackedInline(admin.StackedInline):
    model = SubscriptionTimeRange
    fields = ('starts_at', 'ends_at', 'canceled_at', 'payed_at', 'payment_id')
    extra = 0


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_payed')
    list_filter = ('user__is_staff', IsSubscriptionPayedFilter)
    search_fields = ('id', 'user__username')
    inlines = [SubscriptionTimeRangeStackedInline]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_wallet', 'to_wallet', 'amount')
    list_filter = (('created_at', DateTimeRangeFilter),)
    search_fields = ('from_wallet__id', 'to_wallet__id', 'amount')
    readonly_fields = ('created_at',)
    fields = ('created_at', 'from_wallet', 'to_wallet', 'amount')
