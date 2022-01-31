from django.urls import path
from django.views.generic import TemplateView

from .views import (ChangePasswordView, ConnectExtensionView, RegisterView,
                    Spsp4View, StatusView, SubscriptionActivateView,
                    SubscriptionCancelView, SubscriptionChargedView,
                    TransferView)

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('change-password', ChangePasswordView.as_view()),
    path('connect-extension', ConnectExtensionView.as_view()),
    path('status', StatusView.as_view()),
    path('transfer', TransferView.as_view()),
    path('subscription/activate', SubscriptionActivateView.as_view()),
    path('subscription/charged', SubscriptionChargedView.as_view()),
    path('subscription/cancel', SubscriptionCancelView.as_view()),
]

spsp4_urlpatterns = [
    path('testmonetization', TemplateView.as_view(template_name="testmonetization.html")),
    path('~<str:username>', Spsp4View.as_view()),
    path('=<str:uid>', Spsp4View.as_view()),
]
