from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import *

class CustomRegisterForm(UserCreationForm):
    # Тут можно переопределять поля регистрации, то есть поля username и email являются моими собственными
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)

    # Метод который создает ошибку, если пользователь с таким email уже существует
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже используется.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    #password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Пароль'}))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


class FilterPostForm(forms.Form):
    astronomy = forms.BooleanField(required=False)
    marketing = forms.BooleanField(required=False)
    philosophy = forms.BooleanField(required=False)



