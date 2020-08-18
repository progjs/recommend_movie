from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Movie, Actor, Genre, Comment, UserDetail
from .forms import CommentForm, UserForm, UserDetailForm


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
    user_form = UserForm()
    userdetail_form = UserDetailForm()
    return render(request, 'registration/signup.html', {'user_form': user_form, 'userdetail_form': userdetail_form})


#             post = Post.objects.create(author=User.objects.get(username=request.user.username),
#                                        published_date=timezone.now(), title=form.cleaned_data['title'],
#                                        text=form.cleaned_data['text'])
def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userdetail_form = UserDetailForm(request.POST)
        print(request.method)

        if not (user_form.is_valid() and userdetail_form.is_valid()):
            print("Valid NOOOOOOOOOOOOOOOOOOOOOOOO")

        if user_form.is_valid() and userdetail_form.is_valid():
            # if user_form.password == user

            print('VALID OK~~~~~~~~~~~~~~~~~~~~~~~')
            print("UserForm data : ", user_form.cleaned_data)
            print("UserDetailForm data : ", userdetail_form.cleaned_data)
            # user = user_form.save()
            # user_detail = userdetail_form.save(commit=False)
            # user_detail.user = user
            # user_detail.save()

            user = User.objects.create(username=user_form.cleaned_data['username'],
                                       password=user_form.cleaned_data['password'],
                                       first_name=user_form.cleaned_data['first_name'],
                                       email=user_form.cleaned_data['email'],
                                       )

            user.userdetail.sex = userdetail_form.cleaned_data['sex']
            user.userdetail.birth = userdetail_form.cleaned_data['birth']
            user.userdetail.favorite_genre = userdetail_form.cleaned_data['favorite_genre']
            user.save()

            return render(request, 'registration/login.html')
        else:
            user_form = UserForm()
            userdetail_form = UserDetailForm()
        return render(request, 'registration/signup.html', {'user_form': user_form, 'userdetail_form': userdetail_form})
