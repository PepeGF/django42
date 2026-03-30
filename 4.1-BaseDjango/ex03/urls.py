from django.urls import path
from . import views

# App-level URL patterns for ex01. Add routes here.
urlpatterns = [
    path('', views.table_view, name='ex03-table'),
]
