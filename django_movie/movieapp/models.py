from django.db import models
from django.utils import timezone


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)  # 유효성검사 함수
    score = models.FloatField()
    nation = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    audience = models.IntegerField()
    plot = models.TextField()
    like = models.IntegerField()
    dislike = models.IntegerField()
    release_year = models.IntegerField()

    def __str__(self):
        return self.title


class Genre(models.Model):
    movie = models.ForeignKey('movieapp.Movie', on_delete=models.CASCADE, related_name='genres')
    genre = models.CharField(max_length=200)

    def __str__(self):
        return self.genre


class Actor(models.Model):
    movie = models.ForeignKey('movieapp.Movie', on_delete=models.CASCADE, related_name='actors')
    actor = models.CharField(max_length=200)

    def __str__(self):
        return self.actor


class Comment(models.Model):
    movie = models.ForeignKey('movieapp.Movie', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    comment = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['published_date']

    def __str__(self):
        return self.comment
