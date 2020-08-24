from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('genre/', views.genre_filter, name='genre_filter'),
    path('', views.about, name='about'),
    path('', views.contact, name='contact'),
    path('', views.services, name='services'),
    path('', views.works, name='works'),
    path('movie_detail/<int:pk>/', views.movie_detail, name='movie_detail'),
    # path('accounts/signup/', views.signup, name='signup'),
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/signup/', views.create_user, name='create_user'),
    path('wishlist/', views.add_wishlist, name='add_wishlist'),
    path('search', views.search_movie, name='search_movie'),

]
