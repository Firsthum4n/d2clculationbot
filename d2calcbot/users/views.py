from django.http import  HttpResponse
from django.shortcuts import render

from users.forms import LoginUserForm


def login_user(request):
    form = LoginUserForm
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    return HttpResponse("logout")