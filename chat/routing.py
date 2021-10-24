from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/chat/<str:username>/', consumers.ChatConsumer.as_asgi()),
]