import base64
import traceback

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.exceptions import (APIException, ParseError,
                                       PermissionDenied)
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from .exceptions import (ActiveSubscriptionExists, LowBalance,
                         NoActiveSubscription, invalid_receiver_error)
from .models import Subscription, Wallet
from .serializers import (ChangePasswordSerializer, RegisterSerializer,
                          WalletSerializer)
from .utils import (activate_subscription, calculate_receivers_percentage,
                    cancel_subscription, transfer_tokens)

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not isinstance(self.request.data, dict):
            raise ParseError

        if self.request.auth:
            raise PermissionDenied

        serializer = RegisterSerializer(
            data=self.request.data,
            context={ 'request': self.request },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({ 'success': True })


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
        except (DjangoValidationError, Wallet.DoesNotExist):
            raise RestValidationError({ field_name: ['This field must be a valid Wallet id.'] })
        return wallet

    def post(self, request):
        if not isinstance(self.request.data, dict):
            raise ParseError

        amount = self._get_amount(self.request.data, 'amount')
        from_wallet = self._get_wallet(self.request.data, 'from')
        to_wallet = self._get_wallet(self.request.data, 'to')

        if from_wallet == to_wallet:
            raise RestValidationError({ api_settings.NON_FIELD_ERRORS_KEY: ['Wallet ids `from` and `to` must not be the same.'] })

        if not self.request.user.is_staff and from_wallet.user != self.request.user:
            raise PermissionDenied

        if from_wallet.amount < amount:
            raise LowBalance

        transfer_tokens(from_wallet, to_wallet, amount)

        return Response({ 'success': True })


class SubscriptionActivateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if Subscription.objects.filter(user=self.request.user).current().payed().exists():
            raise ActiveSubscriptionExists

        try:
            r = requests.get(
                f'{settings.PAYMENT_API_BASE}/api/generic-donation/{settings.PAYMENT_CAMPAIGN_ID}/',
                params={ 'customer_id': self.request.user.customer_id },
                timeout=30,
            )
            data = r.json()
            token = data['token']
            customer_id = data['customer_id']
        except Exception as e:
            print('Exception in SubscriptionActivateView GET:')
            traceback.print_exc()
            raise APIException

        if not self.request.user.customer_id:
            self.request.user.customer_id = customer_id
            self.request.user.save()

        return Response({ 'token': token })

    def post(self, request):
        if not isinstance(self.request.data, dict):
            raise ParseError

        if Subscription.objects.filter(user=self.request.user).current().payed().exists():
            raise ActiveSubscriptionExists

        nonce = self.request.data.get('nonce')
        if nonce is None or nonce == '':
            raise RestValidationError({ 'nonce': ['This field may not be blank.'] })

        try:
            r = requests.post(
                f'{settings.PAYMENT_API_BASE}/api/generic-donation/subscription/{settings.PAYMENT_CAMPAIGN_ID}/',
                json={
                    'nonce': nonce,
                    'amount': 5,
                    'email': self.request.user.email,
                },
                timeout=30,
            )
            data = r.json()
            payment_token = data['subscription_id']
        except Exception as e:
            print('Exception in SubscriptionActivateView POST:')
            traceback.print_exc()
            raise APIException

        activate_subscription(self.request.user, payment_token)

        return Response({ 'success': True })


class SubscriptionCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not Subscription.objects.filter(user=self.request.user).current().payed().exists():
            raise NoActiveSubscription

        subscription = Subscription.objects.get(user=self.request.user)
        time_range = subscription.time_ranges.current().payed().first()

        try:
            r = requests.post(
                f'{settings.PAYMENT_API_BASE}/api/generic-donation/cancel-subscription/',
                json={
                    'customer_id': self.request.user.customer_id,
                    'subscription_id': time_range.payment_token,
                },
                timeout=30,
            )
            data = r.json()
            assert data['msg'] == 'subscription canceled', "bad response msg"
        except Exception as e:
            print('Exception in SubscriptionCancelView POST:')
            traceback.print_exc()
            raise APIException

        cancel_subscription(self.request.user)

        return Response({ 'success': True })


class Spsp4View(APIView):
    renderer_classes = [JSONRenderer]
    permission_classes = [AllowAny]

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
        except (DjangoValidationError, User.DoesNotExist):
            return None

    @staticmethod
    def _get_wallet(user):
        if not user:
            return None
        try:
            return Wallet.objects.get(user=user)
        except (DjangoValidationError, Wallet.DoesNotExist):
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
