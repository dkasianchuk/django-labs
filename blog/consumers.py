from channels.generic.websocket import JsonWebsocketConsumer
from users.models import ConnectedUsers
from asgiref.sync import async_to_sync
from rest_framework.authtoken.models import Token
from django.db.models import F


def update_count(connected_user, delta):
    connected_user.count = F('count') + delta
    connected_user.save()


class ConsumerMixin(JsonWebsocketConsumer):
    group_name = None

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
            connected_user = ConnectedUsers.objects.get(user=self.scope['user'])
            if connected_user.count == 1:
                connected_user.delete()
            else:
                update_count(connected_user, -1)

    def handle_data_request(self, content):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {'type': 'message.handle', 'content': content})

    def get_group_name(self, username):
        return "%s_group" % username

    def receive_json(self, content, **kwargs):
        try:
            if content['type'] == 'data':
                if self.scope['user'].is_authenticated:
                    self.handle_data_request(content)
                else:
                    self.send_json({'type': 'error', 'text': 'No authenticated.'})
            elif content['type'] == 'auth' and not self.scope['user'].is_authenticated:
                current_user = Token.objects.get(key=content['token']).user
                self.group_name = self.get_group_name(current_user.username)
                connected_user, created = ConnectedUsers.objects.get_or_create(user=current_user)
                if not created:
                    update_count(connected_user, 1)
                async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
                self.scope['user'] = current_user
                self.send_json({'type': 'auth', 'result': True})
        except Exception as e:
            self.send_json({'type': 'error', 'text': repr(e)})

    def message_handle(self, event):
        self.send_json(event['content'])


class BlogConsumer(ConsumerMixin):
    def handle_data_request(self, content):
        async_to_sync(self.channel_layer.group_send)(
            self.get_group_name(content['targetUsername']),
            {'type': 'message.handle', 'content': {'type': 'message', 'result': content}})


class TasksConsumer(ConsumerMixin):
    def get_group_name(self, username):
        return f"finished_tasks_{username}"
