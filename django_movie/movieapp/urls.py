from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('filter/', views.index_filter, name='index_filter'),

    ## 회원 계정
    path('accounts/login/', views.login, name='login'),
    path('accounts/logout/', views.logout, name='logout'),
    path('accounts/signup/', views.create_user, name='create_user'),
    path('accounts/password/', views.password, name='password'),
    path('accounts/password/update/', views.update_password, name='update_password'),
    path('accounts/mypage/', views.show_mypage, name='show_mypage'),
    path('accounts/email/update/', views.update_email, name='update_email'),
    path('accounts/favorite_genre/update/', views.update_genre, name='update_genre'),

    ## 추가기능
    path('movie_detail/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie_detail/wishlist/', views.add_wishlist, name='add_wishlist'),
    path('search/', views.search_movie, name='search_movie'),
    path('wishlist/', views.show_wishlist, name='show_wishlist'),

    ## 댓글 CRUD
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('comment/remove/<int:pk>/<int:comment_id>/', views.remove_comment, name='remove_comment'),
]
