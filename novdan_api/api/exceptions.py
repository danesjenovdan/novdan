from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response


class ActiveSubscriptionExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Active subscription already exists.'
    default_code = 'active_subscription_exists'


class NoActiveSubscription(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'No active subscription.'
    default_code = 'no_active_subscription'


class LowBalance(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Wallet balance too low.'
    default_code = 'low_balance'


def invalid_receiver_error():
    return Response(
        {
            'id': 'InvalidReceiverError',
            'message': 'Invalid receiver ID',
        },
        status=status.HTTP_404_NOT_FOUND,
        content_type='application/spsp4+json',
    )
