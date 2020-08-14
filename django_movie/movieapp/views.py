from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Movie, Actor, Genre
from .forms import CommentModelForm

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
def add_comment_to_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        # form 객체생성
        form = CommentModelForm(request.POST)
        # form valid check
        if form.is_valid():
            # author, text 값이 comment 객체에 저장
            comment = form.save(commit=False)
            # comment 객체에 매칭
            comment.movie = movie
            # DB에 저장됨
            comment.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = CommentModelForm()
    # return form
    return render(request, 'movieapp/movie_detail.html', {'form': form})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    # genre = get_object_or_404(Genre, pk=pk)
    # genre = Genre.objects.filter(pk=movie.pk)
    # actor = get_object_or_404(Actor, pk=pk)
    return render(request, 'movieapp/movie_detail.html', {'movie':movie})

def signup(request):
    return render(request, 'registration/signup.html')