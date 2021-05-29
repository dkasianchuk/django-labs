from django.urls import re_path
from .consumers import BlogConsumer, TasksConsumer

websocket_urlpatterns = [
    re_path(r'ws/blog/', BlogConsumer.as_asgi()),
    re_path(r'ws/tasks/', TasksConsumer.as_asgi())
]
