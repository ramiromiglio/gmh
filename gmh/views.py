from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views import View

def index(request):
    return render(request, "base_generic.html", context={
        
    })