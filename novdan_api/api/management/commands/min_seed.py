from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from oauth2_provider.models import get_application_model

from ...models import Wallet
from ...utils import generate_tokens_for_month_for_wallet, transfer_tokens

User = get_user_model()
Application = get_application_model()


class Command(BaseCommand):
    help = 'Minimal database seed'

    def handle(self, *args, **options):
        self.stdout.write('Starting ...')

        admin = User.objects.create(
            first_name='djnd',
            username='djnd',
            email='test@test.com',
            is_active=True,
            is_superuser=True,
            is_staff=True,
        )
        admin.set_password('changeme')
        admin.save()

        Application.objects.create(
            user=admin,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
            name='api-client'
        )

        user1 = User.objects.create(
            first_name='user1',
            username='user1',
            email='user1@test.com',
            is_active=True,
        )
        user1.set_password('changeme')
        user1.save()

        user2 = User.objects.create(
            first_name='user2',
            username='user2',
            email='user2@test.com',
            is_active=True,
        )
        user2.set_password('changeme')
        user2.save()

        admin_wallet = Wallet.objects.get(user=admin)
        user1_wallet = Wallet.objects.get(user=user1)
        user2_wallet = Wallet.objects.get(user=user2)

        generate_tokens_for_month_for_wallet(admin_wallet)

        transfer_tokens(admin_wallet, user1_wallet, 5)
        admin_wallet.refresh_from_db() # get updated values from db not CombinedExpression
        transfer_tokens(admin_wallet, user2_wallet, 10)
        admin_wallet.refresh_from_db() # get updated values from db not CombinedExpression

        self.stdout.write('Done')
