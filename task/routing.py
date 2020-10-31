from django.urls import re_path
from task.consumers import CommentConsumer


websocket_urlpatterns = [
    re_path(r'ws/task/(?P<task_id>\w+)/$', CommentConsumer.as_asgi())
]
