from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f"group_{self.group_name}"

        # it's for sync case
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )

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
        if text_data :
            user_data = json.loads(text_data)
            message = user_data["message"]            
            sender = user_data["sender"]
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_group_message',
                    'message': message,
                    'sender' : sender,
                }
            )
    
    async def chat_group_message(self , event):
        if self.user_name != event['sender'] :
            message = event['message']
            sender = event['sender']

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'sender' : sender,
            }))