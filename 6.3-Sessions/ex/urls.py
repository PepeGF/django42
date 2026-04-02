from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("api/nav-text/", views.nav_text, name="nav-text"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("add-tip/", views.add_tip, name="add-tip"),
    path("tip/<int:tip_id>/upvote/", views.tip_upvote, name="tip-upvote"),
    path("tip/<int:tip_id>/downvote/", views.tip_downvote, name="tip-downvote"),
    path("tip/<int:tip_id>/delete/", views.tip_delete, name="tip-delete"),
    path("debug/tips/", views.debug_tips, name="debug-tips"),
]