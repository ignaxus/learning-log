# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

from django.utils import timezone
from learning_logs.models import Topic, Entry


def register(request):
    #if open a new template, create a new registration form
    if request.method != "POST":
        form = UserCreationForm()
    #if post request, save the content
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect("learning_logs:home")

    return render(request, "registration/register.html", {"form": form})

@login_required
def my_account(request):
    #get all information
    topics_count = Topic.objects.filter(owner=request.user).count()

    entries_count = Entry.objects.filter(topic__owner=request.user).count()

    latest_entry = Entry.objects.filter(topic__owner=request.user).order_by("-date_added").first()

    account_age = timezone.now().date() - request.user.date_joined.date()

    context = {
        "topics_count": topics_count,
        "entries_count": entries_count,
        "latest_entry": latest_entry,
        "account_age": account_age.days,
    }

    return render(request, "users/my_account.html", context)