from django.urls import path
from . import views

# App-level URL patterns for ex01. Add routes here.
urlpatterns = [
    path('form/', views.form_view, name='ex02-form'),
]
