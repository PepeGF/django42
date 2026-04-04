import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    room_users = {}

    async def connect(self):
        # posible mejora: comprobar que la sala existe antes de aceptar la conexión
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]

        if not self.user.is_authenticated:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # ex02: send the last 3 messages in chronological order to the user who just joined
        messages = await self.get_last_messages()
        for msg in messages:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": msg["content"],
                        "username": msg["username"],
                    }
                )
            )

        if self.room_name not in self.room_users:
            self.room_users[self.room_name] = set()
        self.room_users[self.room_name].add(self.user.username)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_list",
                "users": sorted(self.room_users[self.room_name]),
            },
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": f"{self.user.username} has joined the chat",
                "username": "system",
            },
        )

    async def disconnect(self, close_code):
        if hasattr(self, "room_name") and self.room_name in self.room_users:
            self.room_users[self.room_name].discard(self.user.username)

            if not self.room_users[self.room_name]:
                del self.room_users[self.room_name]

        if hasattr(self, "room_group_name") and hasattr(self, "user") and self.user.is_authenticated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": f"{self.user.username} has left the chat",
                    "username": "system",
                },
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_list",
                    "users": sorted(self.room_users.get(self.room_name, [])),
                },
            )

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = (data.get("message") or "").strip()
        if not message:
            return

        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "username": self.user.username,
            },
        )

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "username": event["username"],
                }
            )
        )

    async def user_list(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "user_list",
                    "users": event["users"],
                }
            )
        )

    @database_sync_to_async
    def save_message(self, message):
        from .models import ChatMessage, ChatRoom

        room = ChatRoom.objects.get(name=self.room_name)
        ChatMessage.objects.create(room=room, user=self.user, content=message)

    @database_sync_to_async
    def get_last_messages(self):
        from .models import ChatMessage, ChatRoom

        room = ChatRoom.objects.get(name=self.room_name)
        messages = ChatMessage.objects.filter(room=room).order_by("-timestamp")[:3]
        return [
            {"content": msg.content, "username": msg.user.username}
            for msg in reversed(messages)
        ]