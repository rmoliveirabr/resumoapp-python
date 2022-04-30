from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView

from resumoapp.core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name = 'home'),
]
