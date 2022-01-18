import base64

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.exceptions import ParseError
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from .exceptions import (ActiveSubscriptionExists, LowBalance,
                         NoActiveSubscription, invalid_receiver_error)
from .models import Subscription, Transaction, Wallet
from .serializers import ChangePasswordSerializer, WalletSerializer
from .utils import (activate_subscription, calculate_receivers_percentage,
                    cancel_subscription)

User = get_user_model()


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not isinstance(self.request.data, dict):
            raise ParseError

        serializer = ChangePasswordSerializer(
            self.request.user,
            data=self.request.data,
            context={ 'request': self.request },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({ 'success': True })


class StatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.filter(user=self.request.user).first()
        wallet_serializer = WalletSerializer(wallet)

        active_subscription_exists = Subscription.objects.filter(user=self.request.user).current().payed().exists()

        sum, percentages = calculate_receivers_percentage(wallet)

        return Response({
            'wallet': wallet_serializer.data,
            'active_subscription': active_subscription_exists,
            'monetized_split': percentages,
            'monetized_time': sum,
        })


class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _get_amount(data, field_name):
        amount_value = data.get(field_name)
        if amount_value is None or amount_value == '':
            raise RestValidationError({ field_name: ['This field may not be blank.'] })
        try:
            amount = int(amount_value)
        except ValueError:
            raise RestValidationError({ field_name: ['This field must be an integer value.'] })
        if amount < 1:
            raise RestValidationError({ field_name: ['This field must be a positive non-zero integer value.'] })
        return amount

    @staticmethod
    def _get_wallet(data, field_name):
        wallet_id = data.get(field_name)
        if wallet_id is None or wallet_id == '':
            raise RestValidationError({ field_name: ['This field may not be blank.'] })
        try:
            wallet = Wallet.objects.get(id=wallet_id)
        except (ValidationError, Wallet.DoesNotExist):
            raise RestValidationError({ field_name: ['This field must be a valid Wallet id.'] })
        return wallet

    def post(self, request):
        if not isinstance(self.request.data, dict):
            raise ParseError

        amount = self._get_amount(self.request.data, 'amount')
        from_wallet = self._get_wallet(self.request.data, 'from')
        to_wallet = self._get_wallet(self.request.data, 'to')

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

    def post(self, request):
        if not isinstance(self.request.data, dict):
            raise ParseError

        subscription_token = self.request.data.get('subscription_token')
        if subscription_token is None or subscription_token == '':
            raise RestValidationError({ 'subscription_token': ['This field may not be blank.'] })

        if Subscription.objects.filter(user=self.request.user).current().payed().exists():
            raise ActiveSubscriptionExists

        activate_subscription(self.request.user, subscription_token)

        return Response({ 'success': True })


class SubscriptionCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not Subscription.objects.filter(user=self.request.user).current().payed().exists():
            raise NoActiveSubscription

        cancel_subscription(self.request.user)

        return Response({ 'success': True })


class Spsp4View(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = []

    @staticmethod
    def _get_user(uid, username):
        if not uid and not username:
            return None
        elif uid:
            kwargs = { 'uid': uid }
        elif username:
            kwargs = { 'username': username }
        try:
            return User.objects.get(**kwargs)
        except (ValidationError, User.DoesNotExist):
            return None

    @staticmethod
    def _get_wallet(user):
        if not user:
            return None
        try:
            return Wallet.objects.get(user=user)
        except (ValidationError, Wallet.DoesNotExist):
            return None

    @method_decorator(cache_page(60 * 60 * 1))
    def get(self, request, uid=None, username=None):
        user = self._get_user(uid, username)
        if not user:
            return invalid_receiver_error()

        wallet = self._get_wallet(user)
        if not wallet:
            return invalid_receiver_error()

        return Response(
            {
                'destination_account': f'g.novdan.{wallet.id}.transfer',
                'shared_secret': base64.b64encode('TransferDoesNotUseSTREAMProtocol'.encode()), # We don't use STREAM.
            },
            content_type='application/spsp4+json',
        )
