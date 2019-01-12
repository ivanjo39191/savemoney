from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用戶名',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'請輸入用戶名'}))
    password = forms.CharField(label='密碼',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'請輸入密碼'}))


    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError('用戶名或密碼不正確')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class RegisterForm(forms.Form):
    username = forms.CharField(label='用戶名',max_length=10,
                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'請輸入用戶名'}))
    email = forms.EmailField(label='信箱',
                               widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'請輸入信箱'}))
    password = forms.CharField(label='密碼',max_length=12,
                               widget=forms.PasswordInput({'class':'form-control','placeholder':'請輸入密碼'}))
    re_password = forms.CharField(label='密碼',max_length=12,
                                  widget=forms.PasswordInput({'class':'form-control','placeholder':'請再次輸入密碼'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用戶名已存在')
        else:
            return username
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('信箱已存在')
        else:
            return email
    def clean_re_password(self):
        password = self.cleaned_data['password']
        re_password = self.cleaned_data['re_password']
        if password != re_password:
            raise forms.ValidationError('兩次輸入的密碼不一樣')
        else:
            return password