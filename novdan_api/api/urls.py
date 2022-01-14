from django.urls import path, include
from rest_framework import routers

from .views import StatusView, SubscriptionActivateView, SubscriptionCancelView, TransferView


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('status', StatusView.as_view()),
    path('transfer', TransferView.as_view()),
    path('subscription/activate', SubscriptionActivateView.as_view()),
    path('subscription/cancel', SubscriptionCancelView.as_view()),
]
