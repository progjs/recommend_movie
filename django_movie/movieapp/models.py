from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sex = models.CharField(max_length=100, null=True)
    birth = models.DateTimeField(null=True)
    favorite_genre = models.CharField(max_length=500, null=True)
    password2 = models.CharField(max_length=128)


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
    likes_user = models.ManyToManyField(User, through='WishList',
                                        through_fields=('movie', 'user'),
                                        blank=True, related_name='likes_user')

    def __str__(self):
        return self.title

    def calcul_score(self):
        self.score = self.score_sum / self.comment_count

    def count_likes_user(self):
        return self.likes_user.count()


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment = models.TextField(null=True)
    published_date = models.DateTimeField(default=timezone.now)
    comment_score = models.IntegerField(default=0)

    class Meta:
        ordering = ['published_date']

    def __str__(self):
        return self.comment


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    movie = models.ForeignKey('movieapp.Movie', on_delete=models.CASCADE)

    def __str__(self):
        return self.movie
