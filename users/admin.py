# in users/admin.py
from django.contrib import admin
from .models import Attendee

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'registration_date')
    search_fields = ('first_name', 'last_name', 'email')
