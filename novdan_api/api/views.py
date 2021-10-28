from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_409_CONFLICT
from rest_framework.views import APIView

from .models import Wallet, Subscription, Transaction
from .serializers import WalletSerializer
from .utils import calculate_receivers_percentage


class StatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        wallet = Wallet.objects.filter(user=self.request.user).first()
        wallet_serializer = WalletSerializer(wallet)

        active_subscriptions = Subscription.objects.filter(user=self.request.user).active()

        sum, percentages = calculate_receivers_percentage(wallet)

        return Response({
            "wallet": wallet_serializer.data,
            "subscription_active": bool(active_subscriptions.first()),
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

        with transaction.atomic():
            if from_wallet.amount < amount:
                return Response({ "success": False }, status=HTTP_409_CONFLICT)

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
