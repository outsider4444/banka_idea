from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path('chat/<str:slug>/', consumers.ChatConsumer.as_asgi())
]