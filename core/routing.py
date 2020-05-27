from django.urls import re_path
from .consumers import CommentConsumer


websocker_urlpatterns = [
    re_path(r'ws/comment/(?P<room_name>\w+)/$', CommentConsumer)
]