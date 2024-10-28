from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import  HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView

from users.forms import RegisterUserForm, LoginUserForm
from main.utils import DataMixin


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))




class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users:profile')


class Profile(LoginRequiredMixin,DataMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Мой профиль')
        return dict(list(context.items()) + list(c_def.items()))