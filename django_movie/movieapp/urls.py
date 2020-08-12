from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.base, name='index'),
    path('', views.about, name='about'),
    path('', views.contact, name='contact'),
    path('', views.services, name='services'),
    path('', views.works, name='works'),
    path('work_single/', views.work_single, name='work_single'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
]