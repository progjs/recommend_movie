from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Movie, Actor, Genre

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
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    # genre = get_object_or_404(Genre, pk=pk)
    # genre = Genre.objects.filter(pk=movie.pk)
    # actor = get_object_or_404(Actor, pk=pk)
    # print(movie, genre, actor)
    return render(request, 'movieapp/movie_detail.html', {'movie':movie})

def signup(request):
    return render(request, 'registration/signup.html')