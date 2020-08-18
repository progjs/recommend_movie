from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.utils import timezone

from .models import Movie, Actor, Genre, Comment, User
from .forms import CommentForm


# Create your views here.
def index(request):
    user_pk = request.session.get('user')
    if user_pk:
        user = User.objects.get(pk=user_pk)
    # 평점, 좋아요 순으로 정렬
    movie_list = Movie.objects.order_by('score').reverse()[:6]
    return render(request, 'movieapp/index.html', {'movie_list': movie_list, 'user':user})
    return render(request, 'movieapp/index.html', {'user':user})



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

def check_password(pw1, pw2):
    if pw1 == pw2:
        return True
    return False

def login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html')
    if request.method == 'POST':
        user_id = request.POST.get('username')
        password = request.POST.get('password')
        print(user_id, password)
        res_data = {}
        if not (user_id and password):
            res_data['error'] = "모든 칸을 다 입력해주세요"
        else:
            try:
                user = User.objects.get(username = user_id)
            except User.DoesNotExist:
                res_data['error'] = "존재하지 않는 아이디입니다."
            else:
                if check_password(password, user.password):
                    request.session['user'] = user.id
                    return redirect('/')
                else:
                    res_data['error'] = '비밀번호가 틀렸습니다.'
        return render(request, 'registration/login.html', res_data)



# def create_user(request):
    # if request.method == 'POST':
        # form =



