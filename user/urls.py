from django.http import HttpResponse
from django.urls import path

urlpatterns = [
    path('', lambda request: HttpResponse('User details'), name='user-detail')
    #path('<int:id>/', lambda request: HttpResponse('User details'), 'user-detail')
]
