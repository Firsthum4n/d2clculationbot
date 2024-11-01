from django.contrib import admin

from .models import Custom_User, UserGroup


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_username', 'telegram_id', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')


admin.site.register(Custom_User, CustomUserAdmin)

admin.site.register(UserGroup)