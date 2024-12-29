

menu = [
    {'title': 'Главная', 'url_name': 'index' , 'image': 'main/media/nav/home-10-svgrepo-com.svg'},
    {'title': 'Матчи', 'url_name': 'matches', 'image':'main/media/nav/fight-svgrepo-com.svg'},
    {'title': 'История', 'url_name': 'users:history', 'image':'main/media/nav/history-svgrepo-com.svg', 'url':'/users/history/'},
    {'title': 'Меню', 'url_name': 'users:profile', 'image': 'main/media/nav/menu-svgrepo-com.svg', 'url':'/users/profile/'},
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context