from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'ushqim'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]