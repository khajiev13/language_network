from django.urls import re_path
from network import consumers




websocket_urlpatterns = [
    re_path(r'ws/socket-server/',consumers.ChatConsumer.as_asgi())
]