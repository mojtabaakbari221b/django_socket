from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/groupchat/<str:user_name>/to/<str:group_name>/', consumers.ChatConsumer.as_asgi()),
]