from datetime import datetime

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateTimeRangeFilter

from .models import (Subscription, SubscriptionTimeRange, Transaction, User,
                     Wallet)
from .utils import calculate_receivers_percentage


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('url', 'customer_id')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('url',)}),
    )
    search_fields = UserAdmin.search_fields + ('customer_id',)

admin.site.register(User, CustomUserAdmin)


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
            return queryset.payed()
        if self.value() == '0':
            return queryset.exclude(id__in=queryset.payed())
        return queryset


class IsSubscriptionCanceledFilter(admin.SimpleListFilter):
    title = 'is canceled'
    parameter_name = 'is_canceled'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Yes')),
            ('0', _('No')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.canceled()
        if self.value() == '0':
            return queryset.exclude(id__in=queryset.canceled())
        return queryset


class SubscriptionTimeRangeStackedInline(admin.StackedInline):
    model = SubscriptionTimeRange
    fields = ('created_at', 'starts_at', 'ends_at', 'canceled_at', 'payed_at', 'payment_token')
    readonly_fields = ('created_at',)
    extra = 0
    ordering = ('-ends_at',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_payed', 'is_canceled')
    list_filter = ('user__is_staff', IsSubscriptionPayedFilter, IsSubscriptionCanceledFilter)
    search_fields = ('id', 'user__username', 'user__customer_id', 'time_range__payment_token')
    inlines = [SubscriptionTimeRangeStackedInline]

    def is_payed(self, obj):
        return obj.time_ranges.current().payed().exists()

    def is_canceled(self, obj):
        last_time_range = obj.time_ranges.order_by('-ends_at').first()
        if last_time_range:
            return last_time_range.canceled_at is not None
        return False


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_wallet', 'to_wallet', 'amount')
    list_filter = (('created_at', DateTimeRangeFilter),)
    search_fields = ('from_wallet__id', 'to_wallet__id', 'amount')
    readonly_fields = ('created_at',)
    fields = ('created_at', 'from_wallet', 'to_wallet', 'amount')

    def get_urls(self):
        return [
            path('calculate_monthly_split/', self.calculate_monthly_split),
        ] + super().get_urls()

    def calculate_monthly_split(self, request):
        date_string = request.GET.get('date')
        time = timezone.now()
        if date_string:
            time = datetime.strptime(date_string, '%Y-%m-%d')

        sum, percentages = calculate_receivers_percentage(None, time)

        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
           split={'sum': sum, 'percentages': percentages},
           time=time,
        )
        return TemplateResponse(
            request,
            'admin/api/transaction/calculate_monthly_split.html',
            context,
        )
