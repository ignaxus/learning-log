from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.
def home(request):
    return render(request, 'learning_logs/home.html')

@login_required
def topics(request):
    #user can only see their topics, ordered by the date added
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")

    context = {'topics': topics}

    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    #get the topic
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)

    #entries are sorted by the date modified
    entries = topic.entry_set.order_by('-date_modified')

    context = {'topic': topic, 'entries': entries}

    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    #if open this template, create a new form
    if request.method != "POST":
        form = TopicForm()
    #if the request is post, then save the content
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            #do not save directly, the owner should be defined first
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("learning_logs:topics")

    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)

@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)

    #if open this template, create a new form
    if request.method != "POST":
        form = EntryForm()
    #if the request is post, then save the content
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            #do not save directly, the owner should be defined first
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.onwer = request.user
            new_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)

    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)

@login_required
def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)

    #remove the topic and back to topics page
    if request.method == "POST":
        topic.delete()
        return redirect("learning_logs:topics")

    context = {"topic": topic}
    return render(request, "learning_logs/delete_topic.html", context)

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, topic__owner=request.user)

    topic = entry.topic

    #remove the entry and back to topic page
    if request.method == "POST":
        entry.delete()

        return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic,}

    return render(request, "learning_logs/delete_entry.html", context)

@login_required
def edit_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)

    if request.method != "POST":
        #topic content will be in the form
        form = TopicForm(instance=topic)
    else:
        #save the new content
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topics")

    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/edit_topic.html", context)

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        #entry content will be in the form
        form = EntryForm(instance=entry)
    else:
        #save the mew content
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id=topic.id)

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)