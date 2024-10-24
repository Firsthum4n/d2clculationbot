from django.http import  HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from users.forms import LoginUserForm


def login_user(request):
    form = LoginUserForm
    return render(request, 'users/login.html', {'form': form})

# def get_success_url(self):
#     return reverse_lazy('profile')
#
#
# def logout_user(request):
#     logout(request)
#     return redirect('login')

def logout_user(request):
    return HttpResponse("logout")