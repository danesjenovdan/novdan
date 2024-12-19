import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Wallet


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="post_user_save")
def post_user_save(sender, instance, created, **kwargs):
    if created:
        # auto create wallet for new user
        Wallet.objects.create(user=instance)

        # create subscriber and send welcome email
        requests.post(
            f"{settings.PAYMENT_API_BASE}/api/subscribe/",
            json={"email": instance.email, "campaign_id": settings.PAYMENT_CAMPAIGN_ID},
            timeout=30,
        )
