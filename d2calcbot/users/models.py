from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, telegram_id, username, *extra_fields):
        """
        Создает и сохраняет нового пользователя с заданным email и паролем.
        """
        if not telegram_id:
            raise ValueError('The Email field must be set')
        user = self.model(telegram_id, username, *extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, *extra_fields):
        """
        Создает и сохраняет нового суперпользователя с заданным email и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, *extra_fields)


class Custom_User(AbstractUser):
    telegram_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    telegram_username = models.CharField(max_length=255, blank=True, null=True)

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