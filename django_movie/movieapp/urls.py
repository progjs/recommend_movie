from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.about, name='about'),
    path('', views.contact, name='contact'),
    path('', views.services, name='services'),
    path('', views.works, name='works'),
    path('work_single/', views.work_single, name='work_single'),
    path('accounts/signup/', views.signup, name='signup')
]