from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.utils import timezone

from .models import Movie, Actor, Genre, Comment, User, UserDetail
from .forms import CommentForm, UserForm, UserDetailForm


# Create your views here.
def index(request):
    movie_list = Movie.objects.order_by('score').reverse()[:6]
    # if request.session._session:
    #     user_pk = request.session.get('user')
    #     if user_pk:
    #         user = User.objects.get(pk=user_pk)
    #     return render(request, 'movieapp/index.html', {'movie_list': movie_list, 'user': user})
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


def add_comment(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'POST':
        # form 객체생성
        form = CommentForm(request.POST)
        # form valid check
        if form.is_valid():
            comment = form.save(commit=False)
            # comment.author = request.session['user_id']
            comment.author = User.objects.get(username=request.session['user_id'])
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
        return render(request, 'registration/login.html')
    if request.method == 'POST':
        user_id = request.POST['username']
        password = request.POST['password']
        print(user_id, password)
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
                    request.session['user'] = user.id
                    save_session(request, user_id, password)
                    return redirect('/')
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

