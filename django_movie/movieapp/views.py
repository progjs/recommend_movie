from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Movie, Actor, Genre, Comment
from .forms import CommentForm

# Create your views here.
def index(request):
    # movie_list = Movie.objects
    return render(request, 'movieapp/index.html')

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
    #print(request.method)
    if request.method == 'POST':
        # form 객체생성
        form = CommentForm(request.POST)
        # form valid check
        if form.is_valid():
            # author, text 값이 comment 객체에 저장
            comment = form.save(commit=False)
            # print(form)
            # comment 객체에 매칭
            comment.author = User.objects.get(username=request.user.username)
            comment.published_date = timezone.now()
            print(comment.published_date)
            comment.movie = movie
            # print(comment.published_date, comment.movie.title, comment.comment)
            # DB에 저장됨
            print(comment)
            comment.save()

            return redirect('movie_detail', pk=movie.pk)
    #form = CommentForm(instance=movie)
    return render(request, 'movieapp/movie_detail.html', {'commentform': form})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    form = CommentForm(instance=movie)
    # genre = get_object_or_404(Genre, pk=pk)
    # genre = Genre.objects.filter(pk=movie.pk)
    # actor = get_object_or_404(Actor, pk=pk)
    return render(request, 'movieapp/movie_detail.html', {'movie':movie, 'commentform':form })

def signup(request):
    return render(request, 'registration/signup.html')