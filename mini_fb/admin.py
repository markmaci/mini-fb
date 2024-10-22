from django.contrib import admin
from .models import Profile, StatusMessage, Image

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

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_message', 'image_file', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('status_message__first_name', 'status_message__last_name')
    ordering = ('-timestamp',)
