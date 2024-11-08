import jwt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.forms import RegisterUserForm, LoginUserForm
from main.utils import DataMixin

from .models import *




@api_view(['GET'])
def register_user_tg(request):
    if request.method == 'GET':
        telegram_id = request.GET.get('telegram_id')
        telegram_username = request.GET.get('telegram_username')
        redirect_url = f"https://trusight.ru/users/profile"

        if Custom_User.objects.filter(telegram_id=telegram_id).exists():
            user = Custom_User.objects.filter(telegram_id=telegram_id, telegram_username=telegram_username).first()
            login(request, user, backend='users.authentication.TelegramIdAuth')
            return redirect(redirect_url)

        user = Custom_User.objects.create_user(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
        )

        user.save()
        login(request, user, backend='users.authentication.TelegramIdAuth')
        return redirect(redirect_url)
    else:
        return Response({'error': 'Неверный запрос'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def login_user_tg(request):
    if request.method == 'GET':
        telegram_id = request.GET.get('telegram_id')
        telegram_username = request.GET.get('telegram_username')

        if not telegram_id or not telegram_username:
            return Response({'error': 'Отсутствует Telegram ID или username'}, status=status.HTTP_400_BAD_REQUEST)

        user = Custom_User.objects.filter(telegram_id=telegram_id, telegram_username=telegram_username).first()
        if user:
            login(request, user, backend='users.authentication.TelegramIdAuth')
            redirect_url = f"https://trusight.ru/users/profile"
            return redirect(redirect_url)

        return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Неверный запрос'}, status=status.HTTP_400_BAD_REQUEST)





class Profile(LoginRequiredMixin,DataMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Мой профиль')
        return dict(list(context.items()) + list(c_def.items()))

class LogoutView(TemplateView):
    template_name = "users/logout.html"



