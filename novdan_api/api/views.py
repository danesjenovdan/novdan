from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_409_CONFLICT
from rest_framework.views import APIView

from .models import SubscriptionTimeRange, Wallet, Subscription, Transaction
from .serializers import WalletSerializer
from .utils import calculate_receivers_percentage, get_end_of_month, get_start_of_month


User = get_user_model()


class StatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        wallet = Wallet.objects.filter(user=self.request.user).first()
        wallet_serializer = WalletSerializer(wallet)

        active_payed_subscription = Subscription.objects.filter(user=self.request.user).active().payed().first()

        sum, percentages = calculate_receivers_percentage(wallet)

        return Response({
            "wallet": wallet_serializer.data,
            "subscription_payed": bool(active_payed_subscription),
            "monetized_split": percentages,
            "monetized_time": sum,
        })


class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        from_wallet_id = self.request.data.get('from')
        to_wallet_id = self.request.data.get('to')
        amount_string = self.request.data.get('amount')

        if not from_wallet_id or not to_wallet_id or from_wallet_id == to_wallet_id or not amount_string:
            return Response({ "success": False }, status=HTTP_400_BAD_REQUEST)

        try:
            from_wallet = Wallet.objects.get(id=from_wallet_id)
            to_wallet = Wallet.objects.get(id=to_wallet_id)
            amount = int(amount_string)
        except (ValueError, ValidationError, Wallet.DoesNotExist):
            return Response({ "success": False }, status=HTTP_400_BAD_REQUEST)

        if not amount or amount < 1:
            return Response({ "success": False }, status=HTTP_400_BAD_REQUEST)

        if not self.request.user.is_staff and from_wallet.user != self.request.user:
            return Response({ "success": False }, status=HTTP_403_FORBIDDEN)

        if from_wallet.amount < amount:
            return Response({ "success": False }, status=HTTP_409_CONFLICT)

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

        return Response({ "success": True })


class SubscriptionActivateView(APIView):
    permission_classes = [IsAuthenticated]

    # TODO: only allow payment server call this
    def post(self, request, format=None):
        uid = self.request.data.get('uid')
        subscription_token = self.request.data.get('subscription_token')

        if not subscription_token:
            return Response({ "success": False }, status=HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(uid=uid)
        except (ValueError, ValidationError, User.DoesNotExist):
            return Response({ "success": False }, status=HTTP_400_BAD_REQUEST)

        user_subscriptions = Subscription.objects.filter(user=self.request.user)

        active_payed_subscription = user_subscriptions.active().payed().first()
        if active_payed_subscription:
            return Response({ "success": False }, status=HTTP_409_CONFLICT)

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

        return Response({ "success": True })


class SubscriptionCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        active_payed_subscription = Subscription.objects.filter(user=self.request.user).active().payed().first()

        if not active_payed_subscription:
            return Response({ "success": False }, status=HTTP_409_CONFLICT)

        # TODO: cancel payment

        active_payed_subscription.canceled_at = timezone.now()
        active_payed_subscription.save()
        return Response({ "success": True })
