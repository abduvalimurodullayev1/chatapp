import json
from channels.generic.websocket import AsyncWebsocketConsumer
from app.models import ChatGroup, GroupMessage
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

User = get_user_model()


class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f'group_{self.group_id}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender']

        await self.save_message(self.group_id, sender_id, message)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender_id,
        }))

    @sync_to_async
    def save_message(self, group_id, sender_id, message):
        group = ChatGroup.objects.get(id=group_id)
        sender = User.objects.get(id=sender_id)
        GroupMessage.objects.create(group=group, sender=sender, content=message)
