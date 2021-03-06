# coding=utf-8
from django.urls import path, include
from qrcode import views

urlpatterns = [
    path('', views.test.as_view()),
]