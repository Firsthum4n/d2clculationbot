from django import forms
from django.contrib.auth.models import User


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Войти', widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class':'form-input'}))

