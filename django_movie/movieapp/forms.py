from django import forms
from .models import Comment, UserDetail, User


def check_password(pw1, pw2):
    if pw1 != pw2:
        raise forms.ValidationError('비밀번호가 일치하지 않습니다.')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'email', 'username', 'password')


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ('password2', 'sex', 'birth', 'favorite_genre')

