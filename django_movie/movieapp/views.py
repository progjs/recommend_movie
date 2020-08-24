from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.utils import timezone
import json

from .models import Movie, Actor, Genre, Comment, User, UserDetail, WishList
from .forms import UserForm, UserDetailForm


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
    filter_list = Movie.objects.prefetch_related('genres').filter(genres__genre=selected_genre).order_by('score').reverse()[:6]
    movie_list = []
    for movie in filter_list:
        print(movie.title, movie.score)
        info = [movie.title, movie.score]
        movie_list.append(info)
    # return render(request, 'movieapp/index.html', {'movie_list':filter_list})
    return HttpResponse(json.dumps({'genre_movies': movie_list}), content_type="application/json")


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


def add_comment(request, pk):
    if request.method == 'POST':
        new_score = int(request.POST['comment-score'])
        new_comment = request.POST['comment']
        movie = get_object_or_404(Movie, pk=pk)
        user = get_object_or_404(User, username=request.session['user_id'])
        date = timezone.now()
        new_comment = Comment.objects.create(movie=movie, user=user, comment=new_comment, published_date=date, comment_score=new_score)
        new_comment.save()
        movie.score_sum += new_score
        movie.comment_count += 1
        movie.calcul_score()
    return HttpResponseRedirect(request.POST['path'])


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    user_status = 0
    comment_list = Comment.objects.filter(movie__pk=pk).order_by('-published_date')
    # print(request.session.items())
    # user_id가 있는지 확인
    if 'user_id' in request.session.keys():
        user = get_object_or_404(User, username=request.session['user_id'])
        likes_user_list = Movie.objects.filter(pk=pk)
        likes_user = [q['likes_user__username'] for q in likes_user_list.values('likes_user__username')]
        if user.username in likes_user:
            user_status = 1

    return render(request, 'movieapp/movie_detail.html', {'movie': movie, 'user_status': user_status, 'comments': comment_list})


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
    print('이전페이지', request.path)
    if request.method == 'GET':
        return render(request, 'registration/login.html')
    if request.method == 'POST':
        user_id = request.POST['username']
        password = request.POST['password']
        next_path = request.POST['path']
        res_data = {}
        if not (user_id and password):
            res_data['error'] = "모든 칸을 다 입력해주세요"
        else:
            try:
                user = User.objects.get(username=user_id)
            except User.DoesNotExist:
                res_data['error'] = "존재하지 않는 아이디입니다."
            else:
                if check_password(password, user.password):
                    # request.session['user_id'] = user.username
                    save_session(request, user.username, password)
                    return HttpResponseRedirect(request.POST['path'])
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


def add_wishlist(request):
    if request.session['user_id']:
        user = get_object_or_404(User, username=request.session['user_id'])
        movie_id = request.POST.get('movie_id')
        movie = get_object_or_404(Movie, pk=movie_id)
        likes_user_list = Movie.objects.filter(pk=movie_id)
        likes_user = [q['likes_user__username'] for q in likes_user_list.values('likes_user__username')]
        if user.username in likes_user:
            movie.likes_user.remove(user)
            print('삭제함')
            message = 0
        else:
            movie.likes_user.add(user)
            print('추가함')
            message = 1

        print(movie.title, '좋아요 수: ', movie.count_likes_user())
        context = {'like_count': movie.count_likes_user(),
                   'message': message,
                   }
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        context = {'success': False,
                   'error': '로그인이 필요합니다.',
                   'next': request.path
                   }
        return HttpResponse(json.dumps(context), content_type="application/json")
    # return redirect('movie_detail', pk=movie.pk)
