from django.contrib.auth.backends import BaseBackend, UserModel
from users.models import Custom_User

class TelegramIdAuth(BaseBackend):
    def authenticate(self, request, telegram_id=None, telegram_username=None, **kwargs):
        user_model = Custom_User
        if telegram_id and telegram_username:
            try:
                user = user_model.objects.get(telegram_id=telegram_id, telegram_username=telegram_username)
                print(f"User authenticated: {user}")
                return user
            except user_model.DoesNotExist:
                print("User does not exist")
                return None

        return None
