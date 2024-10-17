from typing import Any
from django.contrib import admin
from .models import Game

class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'short_desc')

admin.site.register(Game, GameAdmin)