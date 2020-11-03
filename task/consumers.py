import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from task.models import Comment


class CommentConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.task = self.scope['url_route']['kwargs']['task_id']
        self.task_group_name = 'task_%s' % self.task

        # Join room group
        await self.channel_layer.group_add(
            group=self.task_group_name,
            channel=self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.task_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """ Receive message from WebSocket """

        # get data as a json format and convert to python object
        data = json.loads(text_data)
        print(data, end='\n======================================\n')

        # get message from the data
        comment = data.get('comment')

        # get user
        user = self.scope.get('user')

        # save comment to database
        await self.create_comment(user, self.task, comment)

        response = {
            'comment': comment,
            'user': user.username,
        }

        # send message
        await self.channel_layer.group_send(
            group=self.task_group_name,
            message={
                'type': 'task_comment',
                'text': json.dumps(response),
            }
        )

    async def task_comment(self, event):
        """ Receive message from room group """

        text_data = event['text']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(text_data))

    @database_sync_to_async
    def create_comment(self, user, task, comment):
        return Comment.objects.create(
            username=user,
            task_id=task,
            comment_content=comment,
        )
