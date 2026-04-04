from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import ChatRoom


class RoomListView(LoginRequiredMixin, TemplateView):
    template_name = "chat/rooms.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rooms"] = ChatRoom.objects.all().order_by("name")
        return context


class RoomView(LoginRequiredMixin, TemplateView):
    template_name = "chat/room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = get_object_or_404(ChatRoom, name=self.kwargs["room_name"])
        context["room"] = room
        return context