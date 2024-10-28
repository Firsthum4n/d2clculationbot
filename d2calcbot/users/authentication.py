from django.contrib.auth.backends import BaseBackend, UserModel

from users.models import Custom_User


class TelegramIdAuth(BaseBackend):
    def authenticate(self, request, username=None, **kwargs):
        user_model = Custom_User

        user = UserModel._default_manager.get_by_natural_key(telegram_id=username)
        return user