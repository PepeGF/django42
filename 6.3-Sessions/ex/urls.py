from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    # path('index/', views.index, name='index'),
    # path('ex/index/', views.index, name='ex-index'),
]