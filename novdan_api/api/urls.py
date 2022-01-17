from django.urls import include, path
from rest_framework import routers

from .views import (ChangePasswordView, StatusView, SubscriptionActivateView,
                    SubscriptionCancelView, TransferView)

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('change-password', ChangePasswordView.as_view()),
    path('status', StatusView.as_view()),
    path('transfer', TransferView.as_view()),
    path('subscription/activate', SubscriptionActivateView.as_view()),
    path('subscription/cancel', SubscriptionCancelView.as_view()),
]
