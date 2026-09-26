from datetime import date

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.urls import reverse
from django.utils import timezone

from .models import Entry


def admin_dashboard(request):
    if request.path != reverse('admin:index') or not request.user.is_superuser:
        return {}

    user_model = get_user_model()
    context = {
        'admin_user_count': user_model.objects.count(),
        'admin_active_user_count': user_model.objects.filter(is_active=True).count(),
        'admin_inactive_user_count': user_model.objects.filter(is_active=False).count(),
        'admin_recent_users': user_model.objects.order_by('-date_joined')[:5],
    }

    today = timezone.localdate()
    current_month = today.replace(day=1)
    month_points = []
    for months_ago in range(11, -1, -1):
        month_index = current_month.year * 12 + current_month.month - 1 - months_ago
        month_points.append(date(month_index // 12, month_index % 12 + 1, 1))

    earliest_month = month_points[0]
    monthly_totals = {
        (row['date__year'], row['date__month']): row['total']
        for row in Entry.objects.filter(date__gte=earliest_month, date__lte=today)
        .values('date__year', 'date__month')
        .annotate(total=Count('id'))
    }
    emotion_totals = {
        row['emotion']: row['total']
        for row in Entry.objects.values('emotion').annotate(total=Count('id'))
    }

    context['admin_analytics'] = {
        'total_entries': Entry.objects.count(),
        'emotion_labels': [label for _, label in Entry.EMOTION_CHOICES],
        'emotion_values': [emotion_totals.get(value, 0) for value, _ in Entry.EMOTION_CHOICES],
        'month_labels': [month.strftime('%b %Y') for month in month_points],
        'monthly_values': [monthly_totals.get((month.year, month.month), 0) for month in month_points],
    }
    return context
