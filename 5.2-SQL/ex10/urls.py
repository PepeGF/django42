from django.urls import path
from . import views

urlpatterns = [
    path('', views.display, name='ex10_display'),
]