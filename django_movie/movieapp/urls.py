from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    ## 회원 계정
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/signup/', views.create_user, name='create_user'),

    ## 추가기능
    path('movie_detail/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('wishlist/', views.add_wishlist, name='add_wishlist'),
    path('search', views.search_movie, name='search_movie'),
    path('wordcloud/<int:pk>/', views.add_wordcloud, name='add_wordcloud'),
    # path('genre/', views.genre_filter, name='genre_filter'),

    ## 댓글 CRUD
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('comment/remove/<int:pk>/<int:comment_id>/', views.remove_comment, name='remove_comment'),
]
