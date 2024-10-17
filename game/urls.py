from django.db import models
from django.urls import reverse, path
from .views import *
from django.views.generic import RedirectView

urlpatterns = [
    path('',             GameListView.as_view(),       name='game-list'),
    path('<pk>/',        GameModsListView.as_view(),   name='game-mods-list'),
    path('<pk>/create/', GameModsCreateRedirectView.as_view()),
]