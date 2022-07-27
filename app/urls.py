from django.contrib import admin
from django.urls import path

from app.views import render_page

urlpatterns = [
    path('', render_page),
]
