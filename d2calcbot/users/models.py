from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self,telegram_username, telegram_id, *extra_fields):
        """
        Создает и сохраняет нового пользователя с заданным telegram_id и username.
        """
        if not telegram_id:
            raise ValueError('The telegram_id field must be set')
        if not telegram_username:
            raise ValueError('The username field must be set')
        user = self.model(telegram_id=telegram_id, telegram_username=telegram_username, *extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_username, telegram_id, password=None,is_superuser=True):
        """
        Создает и сохраняет нового суперпользователя с заданным username и email.
        """



        user = self.model(telegram_username=telegram_username, telegram_id=telegram_id)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def check_password(self, user, raw_password):
        return True

    def set_password(self, raw_password):
        pass

class Custom_User(AbstractBaseUser, PermissionsMixin):
    telegram_username = models.CharField(max_length=255, blank=True, null=True)
    telegram_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)


    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        related_name='custom_user_set', # Изменяем имя обратной ссылки
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        related_name='custom_user_set', # Изменяем имя обратной ссылки
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = ['telegram_username']