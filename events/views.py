from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Event, RSVP
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, EventForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def event_list(request):
    events = Event.objects.select_related("organizer")
    user_rsvps = set()
    if request.user.is_authenticated:
        user_rsvps = set(RSVP.objects.filter(user=request.user).values_list("event_id", flat=True))
    return render(request, "events/event_list.html", {"events": events, "user_rsvps": user_rsvps})


@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form.save_m2m()
            return redirect("event_list")
    else:
        form = EventForm()
    return render(request, "events/event_form.html", {"form": form, "title": "Create Event"})


@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = EventForm(instance=event)
    return render(request, "events/event_form.html", {"form": form, "title": "Edit Event"})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.organizer != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        event.delete()
        return redirect("event_list")
    return render(request, "events/event_confirm_delete.html", {"event": event})


@login_required
def rsvp(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        RSVP.objects.get_or_create(user=request.user, event=event)
    return redirect("event_list")


@login_required
def rsvp_cancel(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        RSVP.objects.filter(user=request.user, event=event).delete()
    return redirect("event_list")


@login_required
def my_events(request):
    organized = Event.objects.filter(organizer=request.user)
    attending = Event.objects.filter(rsvps__user=request.user)
    return render(
        request,
        "events/my_events.html",
        {"organized": organized, "attending": attending},
    )
