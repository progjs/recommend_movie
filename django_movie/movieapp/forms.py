from django import forms
from django.forms import Textarea

from .models import Comment, UserDetail, User


def check_password(pw1, pw2):
    if pw1 != pw2:
        raise forms.ValidationError('비밀번호가 일치하지 않습니다.')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'email', 'username', 'password')
        labels = {
            "first_name": "이름",
            "email": "이메일",
            "username": "아이디",
            "password": "비밀번호"
        }
        widgets = {
            "first_name": forms.TextInput,
            "email": forms.EmailInput,
            "username": forms.TextInput,
            "password": forms.PasswordInput
        }


SEX_CHOICES = [('선택안함', '선택안함'),
               ('남자', '남자'),
               ('여자', '여자')]

GENRE_CHOICE = [('드라마', '드라마'), ('판타지', '판타지'), ('공포', '공포'), ('멜로/로맨스', '멜로/로맨스'),
                ('모험', '모험'), ('스릴러', '스릴러'), ('코미디', '코미디'), ('미스터리', '미스터리'),
                ('애니메이션', '애니메이션'), ('범죄', '범죄'), ('SF', 'SF'), ('액션', '액션'), ]


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ('password2', 'sex', 'birth', 'favorite_genre')
        labels = {
            "password2": "비밀번호 확인",
            "sex": "성별",
            "birth": "생년월일",
            "favorite_genre": "좋아하는 영화장르"
        }
        widgets = {
            "password2": forms.PasswordInput,
            "sex": forms.Select(choices=SEX_CHOICES),
            "birth": forms.TextInput,
            "favorite_genre": forms.Select(choices=GENRE_CHOICE)
        }
