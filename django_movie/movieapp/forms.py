from django import forms
from .models import Comment, UserDetail, User


def check_password(pw1, pw2):
    if pw1 != pw2:
        raise forms.ValidationError('비밀번호가 일치하지 않습니다.')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'username', 'password')
        labels = {
            "first_name": "이름",
            "email": "이메일",
            "username": "아이디",
            "password": "비밀번호"
        }


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


