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

    def get_user(self, user_id):
        try:
            return Custom_User.objects.get(pk=user_id)
        except Custom_User.DoesNotExist:
            return None

    def has_perm(self, user_obj, perm, obj=None):
        """
        Проверяет, имеет ли пользователь разрешение.
        """
        if user_obj.is_active and user_obj.has_perm(perm, obj=obj):
            return True
        return False