from django.contrib import admin
from .models import Category, Event, RSVP


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "organizer", "date", "location")
    list_filter = ("date", "categories")
    search_fields = ("title", "description")


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "created_at")
    list_filter = ("created_at",)
