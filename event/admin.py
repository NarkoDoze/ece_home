from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'created_at']
    list_display_links = ['title']