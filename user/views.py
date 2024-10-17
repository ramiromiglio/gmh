from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import User

class ProfileView(DetailView):
    model = User
    pass