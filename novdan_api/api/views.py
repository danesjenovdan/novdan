from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from .exceptions import (ActiveSubscriptionExists, LowBalance,
                         NoActiveSubscription)
from .models import Subscription, SubscriptionTimeRange, Transaction, Wallet
from .serializers import WalletSerializer
from .utils import (calculate_receivers_percentage, get_end_of_month,
                    get_start_of_month)

User = get_user_model()


class StatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        wallet = Wallet.objects.filter(user=self.request.user).first()
        wallet_serializer = WalletSerializer(wallet)

        active_payed_subscription = Subscription.objects.filter(user=self.request.user).active().payed().first()

        sum, percentages = calculate_receivers_percentage(wallet)

        return Response({
            'wallet': wallet_serializer.data,
            'subscription_payed': bool(active_payed_subscription),
            'monetized_split': percentages,
            'monetized_time': sum,
        })


class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_amount(self, field_name, amount_value):
        if amount_value is None or amount_value == '':
            raise RestValidationError({ field_name: ['This field may not be blank.'] })
        try:
            amount = int(amount_value)
        except ValueError:
            raise RestValidationError({ field_name: ['This field must be an integer value.'] })
        if amount < 1:
            raise RestValidationError({ field_name: ['This field must be a positive non-zero integer value.'] })
        return amount

    def _get_wallet(self, field_name, wallet_id):
        if wallet_id is None or wallet_id == '':
            raise RestValidationError({ field_name: ['This field may not be blank.'] })
        try:
            wallet = Wallet.objects.get(id=wallet_id)
        except (ValidationError, Wallet.DoesNotExist):
            raise RestValidationError({ field_name: ['This field must be a valid Wallet id.'] })
        return wallet

    def post(self, request, format=None):
        if not isinstance(self.request.data, dict):
            raise ParseError

        amount = self._get_amount('amount', self.request.data.get('amount'))
        from_wallet = self._get_wallet('from', self.request.data.get('from'))
        to_wallet = self._get_wallet('to', self.request.data.get('to'))

        if from_wallet == to_wallet:
            raise RestValidationError({ api_settings.NON_FIELD_ERRORS_KEY : ['Wallet ids `from` and `to` must not be the same.'] })

        if not self.request.user.is_staff and from_wallet.user != self.request.user:
            raise PermissionDenied

        if from_wallet.amount < amount:
            raise LowBalance

        with transaction.atomic():
            from_wallet.amount = F('amount') - amount
            to_wallet.amount = F('amount') + amount

            new_transaction = Transaction(
                from_wallet=from_wallet,
                to_wallet=to_wallet,
                amount=amount,
            )

            from_wallet.save()
            to_wallet.save()
            new_transaction.save()

        return Response({ 'success': True })


class SubscriptionActivateView(APIView):
    permission_classes = [IsAuthenticated] # TODO: only allow payment server call this

    def _get_user(self, field_name, uid):
        if uid is None or uid == '':
            raise RestValidationError({ field_name: ['This field may not be blank.'] })
        try:
            user = User.objects.get(id=uid)
        except (ValidationError, User.DoesNotExist):
            raise RestValidationError({ field_name: ['This field must be a valid User id.'] })
        return user

    def post(self, request, format=None):
        if not isinstance(self.request.data, dict):
            raise ParseError

        user = self._get_user('uid', self.request.data.get('uid'))

        subscription_token = self.request.data.get('subscription_token')
        if subscription_token is None or subscription_token == '':
            raise RestValidationError({ 'subscription_token': ['This field may not be blank.'] })

        active_payed_subscription = Subscription.objects.filter(user=self.request.user).active().payed().first()
        if active_payed_subscription:
            raise ActiveSubscriptionExists

        with transaction.atomic():
            subscription, created = Subscription.objects.get_or_create(user=user)

            now = timezone.now()
            time_range = subscription.time_ranges.filter(
                starts_at__year=now.year, starts_at__month=now.month,
                ends_at__year=now.year, ends_at__month=now.month,
                payed_at__isnull=True,
            ).first()
            if not time_range:
                time_range = SubscriptionTimeRange.objects.create(
                    starts_at=get_start_of_month(now),
                    ends_at=get_end_of_month(now),
                    subscription=subscription,
                )

            time_range.payed_at = now
            time_range.payment_id = subscription_token
            time_range.save()

        return Response({ 'success': True })


class SubscriptionCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        active_payed_subscription = Subscription.objects.filter(user=self.request.user).active().payed().first()
        if not active_payed_subscription:
            raise NoActiveSubscription

        # TODO: cancel payment

        # FIXME: canceled_at is on subscriptiontimerange not on subscription
        # active_payed_subscription.canceled_at = timezone.now()
        # active_payed_subscription.save()

        return Response({ 'success': True })
