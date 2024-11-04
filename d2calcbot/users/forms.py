from symtable import Class

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginUserForm(forms.Form):
    telegram_id = forms.CharField(label='telegram-id', widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)
    telegram_username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)


class RegisterUserForm(forms.Form):
    telegram_id = forms.CharField(label='telegram-id', widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)
    telegram_username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}), required=True)