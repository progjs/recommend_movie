from django.contrib import admin
from .models import Movie, Genre, Actor, Comment, UserDetail, WishList

# Register your models here.
admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(UserDetail)
admin.site.register(WishList)
