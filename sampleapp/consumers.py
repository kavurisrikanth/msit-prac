import json, logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from django.contrib.auth.models import User

from .models import Message, Room

log = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
         # print(self.scope['url_route'])
         self.room_name = self.scope['url_route']['kwargs']['u']
         self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
         await self.channel_layer.group_add(
             self.room_group_name,
             self.channel_name
         )

         await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        label = text_data_json['room_label']
        sender_username = text_data_json['sender']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'label': label,
                'sender_username': sender_username
            }
        )

    async def chat_message(self, event):

        message = event['message']
        label = event['room_label']
        sender_username = event['sender']

        try:
            room = Room.objects.get(label=label)
            sender = User.objects.get(username=sender_username)
            new_msg = Message.objects.create(room=room, message=message, sender=sender)

            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender_username,
                'first_name': sender.first_name,
                'last_name': sender.last_name,
                'timestamp': json.dumps(new_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                        indent=4, sort_keys=True, default=str)
            }))

        except Room.DoesNotExist:
            log.debug('Room with label %s does not exist!' % label)
            print('Room with label %s does not exist!' % label)
            return
        except User.DoesNotExist:
            log.debug('User with username %s does not exist!' % sender_username)
            print('User with username %s does not exist!' % sender_username)
            return
