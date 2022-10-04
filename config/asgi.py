import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

import teams.consumers
import message.consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('chat/<str:slug>/', teams.consumers.TeamConsumer.as_asgi()),
            path('userchat/<str:room_name>/', message.consumers.ChatConsumer.as_asgi()),
        ])
    )
})
