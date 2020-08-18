from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.BooleanField()
    birth = models.DateTimeField()
    favorite_genre = models.CharField(max_length=400)


@receiver(post_save, sender=User)
def create_user_detail(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_detail(sender, instance, **kwargs):
    instance.userdetail.save()


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)  # 유효성검사 함수
    score = models.FloatField()
    nation = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    audience = models.IntegerField()
    plot = models.TextField()
    comment_count = models.IntegerField()
    score_sum = models.IntegerField()
    release_year = models.IntegerField()

    def __str__(self):
        return self.title

    def calcul_score(self):
        self.score = self.score_sum / self.comment_count


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
