from django.urls import re_path
from .consumers import UpdateConsumer

websocket_urlpatterns = [
    re_path(r'^ws/v1/updates/$', UpdateConsumer.as_asgi()),
]
