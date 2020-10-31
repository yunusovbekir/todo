import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class CommentConsumer(WebsocketConsumer):

    def connect(self):
        self.task = self.scope['url_route']['kwargs']['task_id']
        self.task_group_name = 'task_%s' % self.task

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.task_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.task_group_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        """ Receive message from WebSocket """

        # get data as a json format and convert to python object
        text_data_json = json.loads(text_data)

        # get message from the data
        comment = text_data_json['comment']

        # send message after converting to json
        async_to_sync(self.channel_layer.group_send)(
            self.task_group_name,
            {
                'type': 'task_comment',
                'comment': comment
            }
        )

    def task_comment(self, event):
        """ Receive message from room group """

        comment = event['comment']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'comment': comment
        }))
