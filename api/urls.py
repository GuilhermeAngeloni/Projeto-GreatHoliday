from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetAndUpdate),
    path('new', views.CreateAccount),
]
