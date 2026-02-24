from django.urls import path
from . import views

urlpatterns = [
    path("", views.event_list, name="event_list"),
    path("register/", views.register, name="register"),
    path("event/create/", views.event_create, name="event_create"),
    path("event/<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("event/<int:pk>/delete/", views.event_delete, name="event_delete"),
    path("event/<int:pk>/rsvp/", views.rsvp, name="rsvp"),
    path("event/<int:pk>/rsvp/cancel/", views.rsvp_cancel, name="rsvp_cancel"),
    path("my-events/", views.my_events, name="my_events"),
]
