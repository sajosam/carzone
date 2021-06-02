# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('inquirynquiry/', views.inquiry, name='inquiry'),
 
]
 