from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.about, name='about'),
    path('', views.contact, name='contact'),
    path('', views.services, name='services'),
    path('', views.works, name='works'),
    path('movie_detail/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('comment/<int:pk>/', views.add_comment_to_movie, name='add_comment_to_movie')
]