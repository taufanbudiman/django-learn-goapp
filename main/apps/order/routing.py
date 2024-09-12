# chat/routing.py
from django.urls import re_path

from main.apps.order import consumers

websocket_urlpatterns = [
    re_path(r"ws/notification/(?P<room_name>\w+)/$",
            consumers.NotificationConsumer.as_asgi()),
]