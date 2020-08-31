from django.db.models import Q
from django.db.models.functions import Replace
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, resolve_url, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.utils import timezone
import json
from random import sample

#
from django.db.models import F, Func, Value

from .models import Movie, Actor, Genre, Comment, User, UserDetail, WishList
from .forms import UserForm, UserDetailForm
from django.core import serializers

redirect_path: str = ""


def choice_movies(past_cnt, cur_cnt):
    # past_id = Movie.objects.filter(release_year__lte=2010, score__gte=8.8).values_list('pk', flat=True)
    # choice_id_list = sample(list(past_id), past_cnt)
    # cur_id = Movie.objects.filter(release_year__gt=2010, score__gte=8.5).values_list('pk', flat=True)
    cur_id = Movie.objects.filter(score__gte=8.5).values_list('pk', flat=True)
    choice_id_list = sample(list(cur_id), cur_cnt)
    return choice_id_list


def index(request):
    if 'user_id' in request.session.keys():
        user = get_object_or_404(User, username=request.session['user_id'])
        user_genre = get_object_or_404(UserDetail, user=user).favorite_genre
        genre_movie_id = Movie.objects.filter(genres__genre=user_genre, score__gte=8).values_list('pk', flat=True)
        choice_id = sample(list(genre_movie_id), 3) + choice_movies(2, 6)
    else:
        choice_id = choice_movies(3, 9)
    movie_list = Movie.objects.filter(pk__in=choice_id)
    return render(request, 'movieapp/index.html', {'movie_list': movie_list})


def index_filter(request):
    genre = request.POST.get('genre')
    if genre == 'all':
        genre_movies = Movie.objects.filter(pk__in=choice_movies(3, 9))
    else:
        print('선택한 장르', genre)
        genre_movies = Movie.objects.filter(genres__genre=genre)[0:9]
    genre_dict = {}
    # genre_dict = genre_movies.genres.all()
    # print(genre_dict)
    # print(genre_json)
    movie_list = serializers.serialize('json', genre_movies)
    data = {"movie_data": movie_list, "genre_data": genre_dict}
    return HttpResponse(json.dumps(data), content_type="application/json")


def genre_filter(request):
    # genre_dict = {0:'드라마', 1:'액션', 2:'판타지', 3:'애니메이션', 4:'드라마'}
    selected_genre = request.POST.get('selected_genre')
    # selected_genre = genre_dict[g_id]
    print('선택한 장르 :', selected_genre)
    # filter_list = Genre.objects.filter(genre=selected_genre)
    filter_list = Movie.objects.prefetch_related('genres').filter(genres__genre=selected_genre).order_by(
        'score').reverse()[:6]
    movie_list = []
    for movie in filter_list:
        print(movie.title, movie.score)
        info = [movie.title, movie.score]
        movie_list.append(info)
    # return render(request, 'movieapp/index.html', {'movie_list':filter_list})
    return HttpResponse(json.dumps({'genre_movies': movie_list}), content_type="application/json")


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    user_status = 0
    comment_list = Comment.objects.filter(movie__pk=pk).order_by('-published_date')
    # comment_list = Comment.objects.filter(movie__pk=pk).exclude(comment="").order_by('-published_date')
    # print(request.session.items())
    # user_id가 있는지 확인
    if 'user_id' in request.session.keys():
        user = get_object_or_404(User, username=request.session['user_id'])
        likes_user_list = Movie.objects.filter(pk=pk)
        likes_user = [q['likes_user__username'] for q in likes_user_list.values('likes_user__username')]
        if user.username in likes_user:
            user_status = 1
    return render(request, 'movieapp/movie_comment.html',
                  {'movie': movie, 'user_status': user_status, 'comments': comment_list})
    # return render(request, 'movieapp/movie_detail.html', {'movie': movie, 'user_status': user_status, 'comments': comment_list})


# ------------------- 댓글 CRUD ---------------------
def add_comment(request, pk):
    global redirect_path
    redirect_path = request.GET.get('next', '')

    movie = get_object_or_404(Movie, pk=pk)
    user = get_object_or_404(User, username=request.session['user_id'])

    if request.method == 'POST':
        if Comment.objects.filter(movie=movie, user=user).exists():
            res_data = {'error': "이미 댓글을 작성하셨습니다.\n댓글은 영화마다 한 번만 작성할 수 있습니다.", 'success': False}
            return HttpResponse(json.dumps(res_data), content_type="application/json")

        new_score = int(request.POST.get('comment_score', 0))
        new_comment = request.POST.get('comment', 0)
        print('평점', new_score, '댓글', new_comment)

        date = timezone.now()
        new_comment = Comment.objects.create(movie=movie, user=user, comment=new_comment, published_date=date,
                                             comment_score=new_score)
        new_comment.save()
        print('원래 점수 {}, 댓글 수 {}'.format(movie.score_sum, movie.comment_count))
        movie.score_sum += new_score
        movie.comment_count += 1
        movie.calcul_score()
        movie.save()
        print('변경후 점수 {}, 댓글 수 {}'.format(movie.score_sum, movie.comment_count))
    return HttpResponseRedirect(redirect_path)


def remove_comment(request, pk, comment_id):
    global redirect_path
    redirect_path = request.GET.get('next', '')
    del_comment = get_object_or_404(Comment, pk=comment_id)
    movie = get_object_or_404(Movie, pk=pk)
    movie.score_sum -= del_comment.comment_score
    movie.comment_count -= 1
    movie.calcul_score()
    movie.save()
    del_comment.delete()
    return HttpResponseRedirect(redirect_path)


# ------------------- 회원계정 ---------------------
def signup(request):
    user_form = UserForm()
    userdetail_form = UserDetailForm()
    # return render(request, 'registration/signup.html', {'user_form': user_form, 'userdetail_form': userdetail_form})
    return render(request, 'registration/signup.html')


def check_password(pw1, pw2):
    if pw1 == pw2:
        return True
    return False


def save_session(request, user_id, user_pw):
    request.session['user_id'] = user_id
    request.session['user_pw'] = user_pw


def login(request):
    if request.method == 'GET':
        global redirect_path
        redirect_path = request.GET.get('next', '')
        print('이전 페이지 ', redirect_path)
        return render(request, 'registration/login.html')
    if request.method == 'POST':
        user_id = request.POST['username']
        password = request.POST['password']
        res_data = {}
        if not (user_id and password):
            res_data['error'] = "모든 칸을 다 입력해주세요."
        else:
            try:
                user = User.objects.get(username=user_id)
            except User.DoesNotExist:
                res_data['error'] = "존재하지 않는 아이디입니다."
            else:
                if check_password(password, user.password):
                    save_session(request, user.username, password)
                    return HttpResponseRedirect(redirect_path)
                else:
                    res_data['error'] = '비밀번호가 틀렸습니다.'

        return render(request, 'registration/login.html', res_data)


def logout(request):
    if request.session['user_id']:
        del (request.session['user_id'])
    return redirect('/')


def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        userdetail_form = UserDetailForm(request.POST)
        print(request.method)

        if user_form.is_valid() and userdetail_form.is_valid():
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
    if request.method == 'GET':
        user_form = UserForm()
        userdetail_form = UserDetailForm()
        return render(request, 'registration/signup.html', {'user_form': user_form, 'userdetail_form': userdetail_form})


# ------------------- 추가기능 ---------------------
def add_wishlist(request):
    if request.session['user_id']:
        user = get_object_or_404(User, username=request.session['user_id'])
        movie_id = request.POST.get('movie_id')
        movie = get_object_or_404(Movie, pk=movie_id)

        if movie.likes_user.filter(username=user.username).exists():
            movie.likes_user.remove(user)
            message = 0
        else:
            movie.likes_user.add(user)
            message = 1

        # print(movie.title, '좋아요 수: ', movie.count_likes_user())
        context = {'like_count': movie.count_likes_user(),
                   'message': message,
                   }
        return HttpResponse(json.dumps(context), content_type="application/json")


def search_movie(request):
    search_word = request.GET.get('word')

    fixed_title = Movie.objects.annotate(
        fixed_title=Replace('title', Value(' '), Value('')), )
    fixed_director = Movie.objects.annotate(
        fixed_director=Replace('director', Value(' '), Value('')), )
    fixed_genres = Movie.objects.annotate(
        fixed_genres=Replace('genres__genre', Value(' '), Value('')), )
    fixed_actors = Movie.objects.annotate(
        fixed_actors=Replace('actors__actor', Value(' '), Value('')), )

    if search_word:
        fixed_word = search_word.replace(' ', "")
        movie_list_title = fixed_title.filter(Q(fixed_title__icontains=fixed_word))
        movie_list_director = fixed_director.filter(Q(fixed_director__icontains=fixed_word))
        movie_list_actors = fixed_actors.filter(Q(fixed_actors__icontains=fixed_word))
        movie_list_genres = fixed_genres.filter(Q(fixed_genres__icontains=fixed_word))

        search_movie_list = movie_list_title.union(movie_list_director, movie_list_actors, movie_list_genres)

        return render(request, 'movieapp/search.html', {'movies': search_movie_list, 'search_word': search_word})

    else:
        return render(request, 'movieapp/search.html')


def show_wishlist(request):
    user = get_object_or_404(User, username=request.session['user_id'])
    wishlist = WishList.objects.filter(user_id=user.id).values()

    wish_movies = []
    for wish in wishlist:
        wish_movie = list(Movie.objects.filter(id=wish['movie_id']))
        wish_movies = wish_movies + wish_movie

    return render(request, 'movieapp/wishlist.html', {'wish_movies': wish_movies})
