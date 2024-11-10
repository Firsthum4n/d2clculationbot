import os

from django.conf import settings

from .models import *

menu = [
    {'title': 'Главная', 'url_name': 'index' , 'image': 'media/nav/home-10-svgrepo-com.svg'},
    {'title': 'Матчи', 'url_name': 'index', 'image':'media/nav/fight-svgrepo-com.svg'},
    {'title': 'История', 'url_name': 'users:profile', 'image':'media/nav/history-svgrepo-com.svg'},
    {'title': 'Меню', 'url_name': 'users:profile', 'image': 'media/nav/menu-svgrepo-com.svg'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context