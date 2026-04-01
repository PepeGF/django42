from django.urls import path
from . import views

app_name = 'ex'

urlpatterns = [
    path('', views.home, name='home'),
    path('vote/<int:tip_id>/<str:value>/', views.vote, name='vote'),
    path('delete/<int:tip_id>/', views.delete_tip, name='delete_tip'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
