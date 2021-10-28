from . import consumers
from django.urls import path

websocket_urlpatterns = [
    path('ws/cc/', consumers.ccConsumer.as_asgi()),
]