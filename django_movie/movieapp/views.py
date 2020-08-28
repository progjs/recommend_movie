from django.db.models import Q
from django.db.models.functions import Replace
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, resolve_url, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.utils import timezone
import json

#
from django.db.models import F, Func, Value

from .models import Movie, Actor, Genre, Comment, User, UserDetail, WishList
from .forms import UserForm, UserDetailForm

redirect_path: str = ""


# Create your views here.
def index(request):
    movie_list = Movie.objects.order_by('score').reverse()[:6]
    # if request.session._session:
    #     user_pk = request.session.get('user')
    #     if user_pk:
    #         user = User.objects.get(pk=user_pk)
    #     return render(request, 'movieapp/index.html', {'movie_list': movie_list, 'user': user})
    return render(request, 'movieapp/index.html', {'movie_list': movie_list})


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
    res_data = {}
    movie = get_object_or_404(Movie, pk=pk)
    user = get_object_or_404(User, username=request.session['user_id'])
    if Comment.objects.filter(movie=movie, user=user).exists():
        res_data['error'] = '댓글은 한 번만 작성할 수 있습니다.'
        return HttpResponseRedirect(request.POST['path'])

    if request.method == 'POST':
        new_score = int(request.POST['comment-score'])
        new_comment = request.POST['comment']

        if new_score < 0 or new_score > 10:
            res_data['error'] = '평점을 입력해주세요.'
            return HttpResponseRedirect(request.POST['path'])

        date = timezone.now()
        new_comment = Comment.objects.create(movie=movie, user=user, comment=new_comment, published_date=date,
                                             comment_score=new_score)
        new_comment.save()
        movie.score_sum += new_score
        movie.comment_count += 1
        movie.calcul_score()
    return HttpResponseRedirect(request.POST['path'])


def remove_comment(request, pk, comment_id):
    del_comment = get_object_or_404(Comment, pk=comment_id)
    movie = get_object_or_404(Movie, pk=pk)
    movie.score_sum -= del_comment.comment_score
    movie.comment_count -= 1
    movie.calcul_score()
    del_comment.delete()
    return redirect('movie_detail', pk=pk)


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
    else:
        context = {'success': False,
                   'error': '로그인이 필요합니다.',
                   # 'next': request.path
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
