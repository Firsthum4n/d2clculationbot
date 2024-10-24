from django.http import JsonResponse
from django.views.generic import ListView, View, CreateView, TemplateView

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from .forms import *

import json
from .utils import *
from .calculation import  low_calculation

from .heroes import hero_mod, del_all_heroes_and_ids







class MainHomeView(DataMixin, ListView):
    """
    Класс представления страницы выбоар героеев

    """

    model = Heroes
    template_name = 'main/index.html'
    context_object_name = 'heroes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))




class Heroes_pick(View):

    def post(self, request):
        data = json.loads(request.body)
        radiant_heroes = data.get('radiant_heroes', [])
        request.session['radiant_heroes'] = radiant_heroes

        dire_heroes = data.get('dire_heroes', [])
        request.session['dire_heroes'] = dire_heroes

        result = low_calculation(radiant_heroes, dire_heroes)


        return JsonResponse(
            {'result': result,
             'radiant_heroes': radiant_heroes,}
        )














class Profile(DataMixin, TemplateView):
    template_name = 'main/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Мой профиль')
        return dict(list(context.items()) + list(c_def.items()))


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
        return redirect('profile')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('profile')


def logout_user(request):
    logout(request)
    return redirect('login')