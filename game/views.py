from typing import Any
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, View
from .models import Game
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from mod.models import Mod
from django.urls import reverse
from urllib.parse import quote

class GameListView(ListView):
    model = Game

class GameModsListView(ListView):
    model = Mod
    template_name = 'game/game_mods_list.html'
    
    def get_queryset(self):
        game_id = self.kwargs.get("pk")
        return Mod.objects.filter(related_game=game_id)    

class GameModsCreateRedirectView(View):
    def get(self, request, *args, **kargs):
        url = reverse('mod-create') + '?game=' + quote(kargs['pk'])
        return HttpResponseRedirect(redirect_to=url)