import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from network.consumers import ChatConsumer
from channels.auth import AuthMiddlewareStack
import network.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project4.settings')
print("ASGI is being ran")
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            network.routing.websocket_urlpatterns
        )
    ),
})
