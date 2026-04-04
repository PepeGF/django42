from django.urls import path
from django.http import HttpResponse

app_name = 'chat'

urlpatterns = [
    path('', lambda request: HttpResponse("Chat placeholder"), name='rooms'),
]