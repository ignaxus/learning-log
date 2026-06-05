from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Topic
from .forms import TopicForm, EntryForm

# Create your views here.
def home(request):
    return render(request, 'learning_logs/home.html')

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")

    context = {'topics': topics}

    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)

    entries = topic.entry_set.order_by('-date_added')

    context = {'topic': topic, 'entries': entries}

    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("learning_logs:topics")

    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)

@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)

    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.onwer = request.user
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)
