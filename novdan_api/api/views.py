import base64
import traceback

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from oauth2_provider.contrib.rest_framework.permissions import TokenHasScope
from oauth2_provider.models import (get_access_token_model,
                                    get_application_model,
                                    get_refresh_token_model)
from oauth2_provider.settings import oauth2_settings
from oauthlib.common import generate_token
from rest_framework.exceptions import (APIException, ParseError,
                                       PermissionDenied)
from rest_framework.exceptions import ValidationError as RestValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from sentry_sdk import capture_exception

from .exceptions import (ActiveSubscriptionExists, LowBalance,
                         NoActiveSubscription, invalid_receiver_error)
from .models import Subscription, Wallet
from .serializers import (ChangePasswordSerializer, RegisterSerializer,
                          UserSerializer, WalletSerializer)
from .utils import (activate_subscription, calculate_receivers_percentage,
                    cancel_subscription, get_end_of_last_month,
                    transfer_tokens)

User = get_user_model()
Application = get_application_model()
AccessToken = get_access_token_model()
RefreshToken = get_refresh_token_model()


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


class ConnectExtensionView(APIView):
    def post(self, request):
        user = self.request.user
        application = self.request.auth.application
        expires = timezone.now() + timezone.timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)

        # generate access token that only has `read transfer` scope (no `write`)
        access_token = AccessToken.objects.create(
            user=user,
            scope='read transfer',
            expires=expires,
            token=generate_token(),
            application=application,
        )

        refresh_token = RefreshToken.objects.create(
            user=user,
            token=generate_token(),
            application=application,
            access_token=access_token,
        )

        return Response({
            'access_token': access_token.token,
            'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            'token_type': 'Bearer',
            'scope': access_token.scope,
            'refresh_token': refresh_token.token,
        })


class StatusView(APIView):
    def get(self, request):
        user_serializer = UserSerializer(self.request.user)

        wallet = Wallet.objects.filter(user=self.request.user).first()
        wallet_serializer = WalletSerializer(wallet)

        now_time = timezone.now()
        last_month_time = get_end_of_last_month(now_time)

        subscription = Subscription.objects.filter(user=self.request.user).first()

        if subscription:
            last_time_range = subscription.time_ranges.order_by('-ends_at').first()
            is_canceled = last_time_range is not None and last_time_range.canceled_at is not None

            active_subscription_exists = subscription.time_ranges.current(now_time).payed().exists()

            # check if subscription is canceled and is still active until the
            # end of month
            active_subscription_expires_at = None
            if active_subscription_exists and is_canceled:
                active_subscription_expires_at = last_time_range.ends_at

            # if subscription is not active but was active at the end of last
            # month and we are in the first days of the month, pretend its still
            # active while we wait for payment
            payment_pending = False
            if not active_subscription_exists and not is_canceled:
                if subscription.time_ranges.current(last_month_time).payed().not_canceled().exists():
                    if now_time.day <= settings.PAYMENT_GRACE_PERIOD_DAYS:
                        active_subscription_exists = True
                        payment_pending = True
                    else:
                        payment_pending = True

        # there is no subscription
        else:
            active_subscription_exists = False
            active_subscription_expires_at = None
            payment_pending = False

        sum, percentages = calculate_receivers_percentage(wallet)

        return Response({
            'user': user_serializer.data,
            'wallet': wallet_serializer.data,
            'active_subscription': active_subscription_exists,
            'active_subscription_expires_at': active_subscription_expires_at,
            'payment_pending': payment_pending,
            'monetized_split': percentages,
            'monetized_time': sum,
        })


class TransferView(APIView):
    permission_classes = [IsAuthenticated, TokenHasScope]
    required_scopes = ['transfer']

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
    def get(self, request):
        if Subscription.objects.filter(user=self.request.user).payed().exists():
            raise ActiveSubscriptionExists

        try:
            r = requests.get(
                f'{settings.PAYMENT_API_BASE}/api/generic-donation/{settings.PAYMENT_CAMPAIGN_ID}/',
                params={
                    'customer_id': self.request.user.customer_id,
                    'question_id': settings.PAYMENT_QUESTION_ID,
                    'answer': settings.PAYMENT_QUESTION_ANSWER,
                },
                timeout=30,
            )
            print(f'SubscriptionActivateView GET api response text:')
            print(f'type: {type(r.text)}')
            print(f'r.text: {r.text}')
            data = r.json()
            token = data['token']
            customer_id = data['customer_id']
        except Exception as e:
            capture_exception(e)
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

        if Subscription.objects.filter(user=self.request.user).payed().exists():
            raise ActiveSubscriptionExists

        nonce = self.request.data.get('nonce')
        if nonce is None or nonce == '':
            raise RestValidationError({ 'nonce': ['This field may not be blank.'] })

        try:
            r = requests.post(
                f'{settings.PAYMENT_API_BASE}/api/generic-donation/subscription/{settings.PAYMENT_CAMPAIGN_ID}/',
                json={
                    'nonce': nonce,
                    'amount': settings.PAYMENT_SUBSCRIPTION_AMOUNT,
                    'email': self.request.user.email,
                    'customer_id': self.request.user.customer_id,
                },
                timeout=30,
            )
            print(f'SubscriptionActivateView POST api response text:')
            print(f'type: {type(r.text)}')
            print(f'r.text: {r.text}')
            data = r.json()
            payment_token = data['subscription_id']
        except Exception as e:
            capture_exception(e)
            print('Exception in SubscriptionActivateView POST:')
            traceback.print_exc()
            raise APIException

        activate_subscription(self.request.user, payment_token)

        return Response({ 'success': True })


class SubscriptionChargedView(APIView):
    permission_classes = [AllowAny] # TODO: protect?

    @staticmethod
    def _get_user(data, field_name):
        customer_id = data.get(field_name)
        if customer_id is None or customer_id == '':
            raise RestValidationError({ field_name: ['This field may not be blank.'] })
        try:
            user = User.objects.get(customer_id=customer_id)
        except (DjangoValidationError, User.DoesNotExist):
            raise RestValidationError({ field_name: ['This field must be a valid customer id.'] })
        return user

    @staticmethod
    def _get_kind(data, field_name):
        value = data.get(field_name)
        if value is None or value == '':
            raise RestValidationError({ field_name: ['This field may not be blank.'] })
        return value

    @staticmethod
    def _get_subscription_id(data, field_name, user):
        subscription_id = data.get(field_name)
        if subscription_id is None or subscription_id == '':
            raise RestValidationError({ field_name: ['This field may not be blank.'] })
        # a past payed subscription must already exist if we want to extend it
        subscription = Subscription.objects.filter(user=user).first()
        if not subscription or not subscription.time_ranges.filter(payment_token=subscription_id).exists():
            raise RestValidationError({ field_name: ['This field must be a valid subscription id.'] })
        return subscription_id

    def post(self, request):
        print(f'SubscriptionChargedView POST request.data:')
        print(f'type: {type(self.request.data)}')
        print(f'data: {self.request.data}')

        if not isinstance(self.request.data, dict):
            raise ParseError

        user = self._get_user(self.request.data, 'customer_id')
        kind = self._get_kind(self.request.data, 'kind')
        payment_token = self._get_subscription_id(self.request.data, 'subscription_id', user)

        if kind == 'subscription_charged_successfully':
            activate_subscription(user, payment_token)
        elif kind == 'subscription_canceled':
            cancel_subscription(user, payment_token)
        else:
            raise RestValidationError({ 'kind': ['This field must be a valid kind.'] })

        return Response({ 'success': True })


class SubscriptionCancelView(APIView):
    def post(self, request):
        if not Subscription.objects.filter(user=self.request.user).payed().exists():
            raise NoActiveSubscription

        subscription = Subscription.objects.get(user=self.request.user)

        last_time_range = subscription.time_ranges.payed().order_by('-ends_at').first()
        is_canceled = last_time_range is not None and last_time_range.canceled_at is not None

        if not last_time_range or is_canceled:
            raise NoActiveSubscription

        try:
            r = requests.post(
                f'{settings.PAYMENT_API_BASE}/api/generic-donation/cancel-subscription/',
                json={
                    'customer_id': self.request.user.customer_id,
                    'subscription_id': last_time_range.payment_token,
                },
                timeout=30,
            )
            print(f'SubscriptionCancelView POST api response text:')
            print(f'type: {type(r.text)}')
            print(f'r.text: {r.text}')
            data = r.json()
            assert data['msg'] == 'subscription canceled', "bad response msg"
        except Exception as e:
            capture_exception(e)
            print('Exception in SubscriptionCancelView POST:')
            traceback.print_exc()
            raise APIException

        cancel_subscription(self.request.user, last_time_range.payment_token)

        return Response({ 'success': True })


class Spsp4Renderer(JSONRenderer):
    media_type = 'application/spsp4+json'


class SpspRenderer(JSONRenderer):
    media_type = 'application/spsp+json'


class Spsp4View(APIView):
    renderer_classes = [Spsp4Renderer, SpspRenderer, JSONRenderer]
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
