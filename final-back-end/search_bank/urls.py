
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'search_bank'
urlpatterns = [
    path('', views.search_nearby_banks),
    
    
]
