from django.urls import path, include
from rest_framework import routers

from .views import StatusView, TransferView


router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('status', StatusView.as_view()),
    path('transfer', TransferView.as_view()),
]
