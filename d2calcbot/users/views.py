from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from main.utils import DataMixin

from .models import *

@api_view(['GET'])
def auth_user_tg(request):
    if request.method == 'GET':
        telegram_id = request.GET.get('telegram_id')
        telegram_username = request.GET.get('telegram_username')
        redirect_url = f"https://trusight.ru"

        if not telegram_id or not telegram_username:
            return Response({'error': 'Отсутствует Telegram ID или username'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = Custom_User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={'telegram_username': telegram_username}
        )

        if created:
            print(f"New user created: {user}")
            user.avatar = 'avatars/hand_of_midas.png'  # Устанавливаем стандартный аватар
            user.save()
        else:
            print(f"User authenticated: {user}")

        login(request, user, backend='users.authentication.TelegramIdAuth')
        return redirect(redirect_url)
    else:
        return Response({'error': 'Неверный запрос'}, status=status.HTTP_400_BAD_REQUEST)








class Profile(LoginRequiredMixin,DataMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Мой профиль')
        return dict(list(context.items()) + list(c_def.items()))


class History(TemplateView, DataMixin,):
    template_name = "users/history.html"
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='История')
        return dict(list(context.items()) + list(c_def.items()))

class LogoutView(TemplateView, DataMixin,):
    template_name = "users/logout.html"




