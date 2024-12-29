from django.contrib import admin

from django.contrib import admin
from .models import *


admin.site.register(Heroes)
# admin.site.register(Teams)
admin.site.register(Players)

class PlayersInline(admin.TabularInline):
    model = Players
    extra = 0

@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    inlines = [PlayersInline]
