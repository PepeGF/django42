from . import views
from django.urls import path

app_name = "ex"

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('articles/', views.Articles.as_view(), name='articles'),
    path('articles/<int:pk>/', views.Detail.as_view(), name='article-detail'),
    path('publications/', views.Publications.as_view(), name='publications'),
    path('favourite/', views.Favourite.as_view(), name='favourite'),
]