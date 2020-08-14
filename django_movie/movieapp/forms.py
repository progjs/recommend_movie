from django import forms

def check_password(pw1, pw2):
    if pw1 != pw2:
        raise forms.ValidationError('비밀번호가 일치하지 않습니다.')

# class SignupForm(forms.Form):
#     username = forms.CharField(20)
#     password1 = forms.CharField(30)
#     password2 = forms.CharField(30, validators=[check_password])
#     name = forms.CharField(30)
#     sex = forms.BooleanField()
#     birth = forms.DateTimeField()
#     email = forms.CharField(50)