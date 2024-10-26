from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.defaultfilters import title
from django.urls import reverse_lazy, reverse

from users.forms import LoginUserForm

class Loginuser(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))