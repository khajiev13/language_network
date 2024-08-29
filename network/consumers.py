
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        

        
        
    def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            global sender_id
            global receiver_id
            sender_id = text_data_json['sender_id']
            receiver_id = text_data_json['receiver_id']
            print(f'Sender_id: {sender_id} Message: {message}')


            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

        except json.JSONDecodeError as e:
            print("Something wrong in receive method", e)

    def chat_message(self,event):
        message = event['message']

        self.send(text_data=json.dumps({
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'type':'chat',
            'message':message
        }))
    def typing(self, event):
        typing_message = {
            'type': 'typing',
            'user': event['user']
        }

        self.send(text_data=json.dumps(typing_message))
