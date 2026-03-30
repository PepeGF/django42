from django.urls import path
from . import views

# App-level URL patterns for ex01. Add routes here.
urlpatterns = [
    path('django/', views.django_page, name='ex01-django'),
    path('display/', views.display_page, name='ex01-display'),
    path('templates/', views.templates_page, name='ex01-templates'),
]
