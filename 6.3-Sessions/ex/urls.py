from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("api/nav-text/", views.nav_text, name="nav-text"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("add-tip/", views.add_tip, name="add-tip"),
]