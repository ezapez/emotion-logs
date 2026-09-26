from datetime import timedelta

from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from .models import Entry
from .forms import EntryForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render( request, 'emotion_logs/index.html')




@login_required
def entries(request):
    user_entries = Entry.objects.filter(user=request.user)
    emotion_counts = {
        row['emotion']: row['total']
        for row in user_entries.values('emotion').annotate(total=Count('id'))
    }
    emotion_labels = [label for _, label in Entry.EMOTION_CHOICES]
    emotion_values = [emotion_counts.get(value, 0) for value, _ in Entry.EMOTION_CHOICES]

    today = timezone.localdate()
    start_date = today - timedelta(days=29)
    daily_counts = {
        row['date']: row['total']
        for row in user_entries.filter(date__range=(start_date, today))
        .values('date')
        .annotate(total=Count('id'))
    }
    trend_dates = [start_date + timedelta(days=offset) for offset in range(30)]
    chart_data = {
        'emotion_labels': emotion_labels,
        'emotion_values': emotion_values,
        'trend_labels': [f'{date:%b} {date.day}' for date in trend_dates],
        'trend_values': [daily_counts.get(date, 0) for date in trend_dates],
        'total_entries': user_entries.count(),
        'active_emotions': sum(value > 0 for value in emotion_values),
    }
    return render(request, 'emotion_logs/topics.html', {
        'entries': user_entries,
        'chart_data': chart_data,
    })


@login_required
def new_entry(request):
    form = EntryForm(request.POST or None)
    if form.is_valid():
        entry = form.save(commit=False)
        entry.user = request.user
        entry.save()
        return redirect('emotion_logs:entries')
    return render(request, 'emotion_logs/new_entry.html', {'form': form})
   
@login_required
def edit_entry(request, entry_id):
   entry = get_object_or_404(Entry, id=entry_id, user=request.user)
   form = EntryForm(request.POST or None, instance=entry)
   if form.is_valid():
      form.save()
      return redirect('emotion_logs:entries')
   return render(request, 'emotion_logs/edit_entry.html', {'entry': entry, 'form': form})




      

