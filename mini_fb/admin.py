from django.contrib import admin
from .models import Profile, StatusMessage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('city',)

@admin.register(StatusMessage)
class StatusMessageAdmin(admin.ModelAdmin):
    list_display = ('profile', 'timestamp', 'message')
    search_fields = ('message',)
    list_filter = ('profile', 'timestamp')
