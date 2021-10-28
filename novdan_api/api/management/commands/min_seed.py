from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth import get_user_model
from oauth2_provider.models import get_application_model


User = get_user_model()
Application = get_application_model()


class Command(BaseCommand):
    help = 'Minimal database seed'

    def handle(self, *args, **options):
        self.stdout.write('\n')
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

        self.stdout.write('\n')
        self.stdout.write('Done')
