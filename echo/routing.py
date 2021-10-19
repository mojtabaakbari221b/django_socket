from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/(?P<echo_name>\w+)/$', consumers.EchoConsumer.as_asgi()),
]