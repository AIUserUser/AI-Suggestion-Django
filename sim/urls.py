from django.contrib import admin
from django.urls import path, include
from sim import views

urlpatterns = [
    path('', views.index, name='index'),
    path('suggest', views.suggest, name='suggest'),
]


