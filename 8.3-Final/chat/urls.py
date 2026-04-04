from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("", views.RoomListView.as_view(), name="rooms"),
    path("<str:room_name>/", views.RoomView.as_view(), name="room"),
]