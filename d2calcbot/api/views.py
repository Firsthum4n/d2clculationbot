from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import jwt
from datetime import datetime, timedelta

from users.models import Custom_User

import secrets

# JWT_SECRET_KEY = secrets.token_urlsafe(32)
# print(JWT_SECRET_KEY)

JWT_SECRET_KEY = 'uhgxtj6TqGQ2uerMVsvAuEqEpUg4UmmQBO2h9HQPKq0'

@api_view(['GET'])
def register_user(request):
    if request.method == 'GET':
        telegram_id = request.GET.get('telegram_id')
        telegram_username = request.GET.get('telegram_username')

        if Custom_User.objects.filter(telegram_id=telegram_id).exists():
            return Response({'error': 'Пользователь с таким Telegram ID уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        user = Custom_User.objects.create_user(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
        )

        user.save()
        login(request, user, backend='users.authentication.TelegramIdAuth')

        redirect_url = f"http://127.0.0.1:8000/users/profile"
        return redirect(redirect_url)
    else:
        return Response({'error': 'Неверный запрос'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def login_user(request):
    if request.method == 'GET':
        telegram_id = request.GET.get('telegram_id')
        telegram_username = request.GET.get('telegram_username')

        if not telegram_id or not telegram_username:
            return Response({'error': 'Отсутствует Telegram ID или username'}, status=status.HTTP_400_BAD_REQUEST)

        user = Custom_User.objects.filter(telegram_id=telegram_id, telegram_username=telegram_username).first()
        if user:
            login(request, user, backend='users.authentication.TelegramIdAuth')


            redirect_url = f"http://127.0.0.1:8000/users/profile"
            return redirect(redirect_url)

        return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({'error': 'Неверный запрос'}, status=status.HTTP_400_BAD_REQUEST)