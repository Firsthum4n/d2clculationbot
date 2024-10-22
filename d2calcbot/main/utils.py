from .models import *

menu = [
    {'title': 'Главная', 'url_name': 'index'},
    {'title': 'Профиль', 'url_name': 'profile'},
]


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context