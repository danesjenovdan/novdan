from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Wallet


@receiver(post_save, sender=settings.AUTH_USER_MODEL, dispatch_uid="post_user_save")
def post_user_save(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)