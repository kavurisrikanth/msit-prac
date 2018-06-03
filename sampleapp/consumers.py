import json, logging

from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from .models import Message, Room

log = logging.getLogger(__name__)


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print (text_data_json)
        # print (text_data)
        message = text_data_json['message']
        label = text_data_json['room_label']
        sender_username = text_data_json['sender']

        try:
            room = Room.objects.get(label=label)
            sender = User.objects.get(username=sender_username)

            self.send(text_data=json.dumps({
                'message': message
            }))

            Message.objects.create(room=room, message=message, sender=sender)

        except Room.DoesNotExist:
            log.debug('Room with label %s does not exist!' % label)
            print('Room with label %s does not exist!' % label)
            return
        except User.DoesNotExist:
            log.debug('User with username %s does not exist!' % sender_username)
            print('User with username %s does not exist!' % sender_username)
            return



        # Message.objects.create(message=message)