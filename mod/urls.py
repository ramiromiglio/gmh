from django.db import models
from django.urls import reverse, path
from .views import *

urlpatterns = [
    path('',             ModListView.as_view(),   name='mod-list'),
    path('detail/<pk>/', ModDetailView.as_view(), name='mod-detail'),
    path('create/',      ModCreateView.as_view(), name='mod-create'),
    path('detail/<pk>/download', download_mod_content, name='mod-download'),
]