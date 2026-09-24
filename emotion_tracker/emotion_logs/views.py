from django.shortcuts import get_object_or_404, render, redirect
from .models import Entry
from .forms import EntryForm
from django.contrib.auth.decorators import login_required

def index(request):
    return render( request, 'emotion_logs/index.html')




@login_required
def entries(request):
    user_entries = Entry.objects.filter(user=request.user)
    return render(request, 'emotion_logs/topics.html', {'entries': user_entries})


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




      

