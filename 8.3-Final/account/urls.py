from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.AccountView.as_view(), name='index'),
    path('login/', views.LoginAjaxView.as_view(), name='login'),
    path('logout/', views.LogoutAjaxView.as_view(), name='logout'),
]