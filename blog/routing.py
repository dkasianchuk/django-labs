from django.urls import re_path
from .consumers import BlogConsumer

websocket_urlpatterns = [
    re_path(r'ws/blog/', BlogConsumer.as_asgi()),
]
