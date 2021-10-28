from django.db.models import Sum
from django.utils import timezone

from .models import Transaction


def calculate_receivers_percentage(from_wallet):
    now = timezone.now()
    year = now.year
    month = now.month

    transactions = Transaction.objects.filter(
        from_wallet=from_wallet,
        created_at__year=year,
        created_at__month=month,
    )

    sum = transactions.aggregate(Sum('amount')).get('amount__sum', 0)
    if sum <= 0:
        return 0, []

    results = transactions.values('to_wallet').order_by('to_wallet').annotate(sum=Sum('amount'))
    percentages = [{ 'id': str(result['to_wallet']), 'percentage': result['sum'] / sum } for result in results]

    return sum, percentages


def generate_this_months_tokens(to_wallet):
    now = timezone.now()
    start_of_month = timezone.datetime(now.year, now.month, 1, tzinfo=now.tzinfo)
    end_of_month = timezone.datetime(now.year, now.month + 1, 1, tzinfo=now.tzinfo) - timezone.timedelta(seconds=1)
    seconds = int((end_of_month - start_of_month).total_seconds())

    to_wallet.amount = seconds
    to_wallet.save()
