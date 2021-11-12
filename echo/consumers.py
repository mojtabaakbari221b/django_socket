import json
from channels.generic.websocket import WebsocketConsumer
import random

class EchoConsumer(WebsocketConsumer):
    def connect(self):
        self.scope["session"].name = "mojtaba"
        self.scope["session"].save()
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        print(self.scope["session"].name)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': f"{message} - sent by server"
        }))