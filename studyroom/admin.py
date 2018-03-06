from django.contrib import admin
from .models import Sroom1

@admin.register(Sroom1)
class Sroom1Admin(admin.ModelAdmin):
    list_display = ['reserved', 'sid']
    list_display_links = ['reserved']