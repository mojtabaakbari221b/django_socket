from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f"group_{self.group_name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        if text_data :
            user_data = json.loads(text_data)
            message = user_data["message"]            
            sender = user_data["sender"]
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_group_message',
                'message': message,
                'sender' : sender,
            }
            )
    
    def chat_group_message(self , event):
        if self.user_name != event['sender'] :
            message = event['message']
            sender = event['sender']

            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message,
                'sender' : sender,
            }))