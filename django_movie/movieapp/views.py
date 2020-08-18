from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Movie, Actor, Genre, Comment
from .forms import CommentForm


# Create your views here.
def index(request):
    # 평점, 좋아요 순으로 정렬
    movie_list = Movie.objects.order_by('score').reverse()[:6]
    return render(request, 'movieapp/index.html', {'movie_list': movie_list})


def contact(request):
    name = '영화'
    return render(request, 'movieapp/contact.html')


def about(request):
    name = '영화'
    return render(request, 'movieapp/about.html')


def services(request):
    name = '영화'
    return render(request, 'movieapp/services.html')


def works(request):
    name = '영화'
    return render(request, 'movieapp/works.html')


@login_required
def add_comment(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    print("댓글 작성 ", movie.title)
    print(request.method)
    if request.method == 'POST':
        # form 객체생성
        form = CommentForm(request.POST)
        # form valid check
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = User.objects.get(username=request.user.username)
            comment.published_date = timezone.now()
            comment.movie = movie
            comment.save()
            return redirect('movie_detail', pk=movie.pk)
    return render(request, 'movieapp/movie_detail.html', {'commentform': form})


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.calcul_score()
    form = CommentForm(instance=movie)
    return render(request, 'movieapp/movie_detail.html', {'movie': movie, 'commentform': form})


def signup(request):
    return render(request, 'registration/signup.html')

# def create_user(request):
    # if request.method == 'POST':
        # form =



