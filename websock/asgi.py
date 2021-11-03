"""
ASGI config for websock project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter , URLRouter
from django.core.asgi import get_asgi_application
from echo.routing import websocket_urlpatterns as echo_websocket_urlpatterns
from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from cryptocurrency.routing import websocket_urlpatterns as cc_websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'websock.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # echo_websocket_urlpatterns,
            chat_websocket_urlpatterns,
            # cc_websocket_urlpatterns,
        )
    ),
})