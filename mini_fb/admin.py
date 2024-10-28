from django.contrib import admin
from .models import Profile, StatusMessage, Image, Friend

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
    search_fields = ('status_message__profile__first_name', 'status_message__profile__last_name')
    ordering = ('-timestamp',)

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('profile1', 'profile2', 'timestamp')
    search_fields = ('profile1__first_name', 'profile1__last_name', 'profile2__first_name', 'profile2__last_name')
    list_filter = ('timestamp',)
