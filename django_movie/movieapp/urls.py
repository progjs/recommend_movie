from django.urls import path
from . import views


urlpatterns = [
    path('', views.base, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('work/', views.works, name='works'),
    path('work_single/', views.work_single, name='work_single'),
]