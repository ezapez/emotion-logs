from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404



# Create your views here.

def index(request):
    return render( request, 'emotion_logs/index.html')




@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render( request, 'emotion_logs/topics.html',context)

@login_required
def topic(request, topic_id):
 """Show a single topic and all its entries."""
 topic = Topic.objects.get(id=topic_id)
 # make sure the topic belongs to current user 
 if topic.owner != request.user:
    raise Http404
 entries = topic.entry_set.order_by('-date_added')
 context = {'topic': topic, 'entries': entries}
 return render(request, 'emotion_logs/topic.html', context)

@login_required
def new_topic(request):
   if request.method != 'POST':
      # no data submitted; create a blank form. 
      form = TopicForm()
   else:
        # post data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
           new_topic = form.save(commit=False)
           new_topic.owner = request.user
           new_topic.save()
           return redirect('emotion_logs:topics')
    # display a blank or invalid form.
   context = {'form': form}
   return render(request, 'emotion_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
   """ Add a new entry for a particular topic """
   topic = Topic.objects.get(id=topic_id)

   if request.method != 'POST':
      # no data submitted; create a blank form
      form = EntryForm()
   else:
      # post data submitted; process data.
      form = EntryForm(data=request.POST)
      if form.is_valid():
         new_entry = form.save(commit=False)
         new_entry.topic = topic
         new_entry.save()
         return redirect('emotion_logs:topic', topic_id=topic_id)
      
    #display a blank or invalid form 
   context = {'topic': topic, 'form': form }
   return render(request, 'emotion_logs/new_entry.html', context)
   
@login_required
def edit_entry(request, entry_id):
   entry = Entry.objects.get(id=entry_id)
   topic = entry.topic
   if topic.owner != request.user:
    raise Http404

   if request.method != "POST":
      form = EntryForm(instance=entry)
   else:
       form = EntryForm(instance=entry, data=request.POST)
       if form.is_valid():
            form.save()
            return redirect('emotion_logs:topic', topic_id=topic.id)
   context  = {'entry': entry, 'topic': topic, 'form': form}
   return render(request, 'emotion_logs/edit_entry.html', context)




      

