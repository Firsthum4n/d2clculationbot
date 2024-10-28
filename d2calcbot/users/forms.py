from symtable import Class

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from users.models import Custom_User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    telegram_id = forms.CharField(label='telegram-id', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Custom_User
        fields = ('username', 'telegram_id')




class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    telegram_id = forms.CharField(label='telegram-id', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = Custom_User
        fields = ('username', 'telegram_id')
