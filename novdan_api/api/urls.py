from django.urls import path

from .views import (ChangePasswordView, Spsp4View, StatusView,
                    SubscriptionActivateView, SubscriptionCancelView,
                    TransferView)

urlpatterns = [
    path('change-password', ChangePasswordView.as_view()),
    path('status', StatusView.as_view()),
    path('transfer', TransferView.as_view()),
    path('subscription/activate', SubscriptionActivateView.as_view()),
    path('subscription/cancel', SubscriptionCancelView.as_view()),
]

spsp4_urlpatterns = [
    path('~<str:username>', Spsp4View.as_view()),
    path('<str:uid>', Spsp4View.as_view()),
]
