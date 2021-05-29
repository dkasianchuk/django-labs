import datetime
from celery import shared_task, Task
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail
from django.conf.global_settings import EMAIL_HOST_USER
from .models import Post, Comment


class CallbackTaskMixin(Task):
    task_name = None

    def on_success(self, result, task_id, args, kwargs):
        self.report('successTaskResult', task_id, args, 'result', result)

    def on_failure(self, exc, task_id, args, kwargs, info):
        self.report('errorTaskResult', task_id, args, 'text', repr(exc))

    def report(self, response_type, task_id, args, additional_field, additional_value):
        channel_layer = get_channel_layer()
        if not channel_layer:
            return

        async_to_sync(channel_layer.group_send)(
            # username is the first element of args
            f"finished_tasks_{args[0]}",
            {
                'type': 'message.handle',
                'content':
                    {'type': response_type,
                     'taskId': task_id,
                     'taskName': self.task_name,
                     'taskArgs': args,
                     'finishTime': str(datetime.datetime.now()),
                     additional_field: additional_value},
            }
        )

    def run(self, *args, **kwargs):
        pass


class ActivitiesTask(CallbackTaskMixin):
    task_name = 'activities'


class EmailsTask(CallbackTaskMixin):
    task_name = 'emails'


@shared_task(name='activities', base=ActivitiesTask)
def get_user_activities(username):
    return {'username': username,
            'posts': count_from_model(Post, username),
            'comments': count_from_model(Comment, username)}


def count_from_model(model, username):
    return model.objects.filter(author__username=username).count()


@shared_task(name='emails', base=EmailsTask)
def send_follow_emails(username, receivers):
    message = f'Hello!!!\nMy name is {username}. This letter is invitation to read my blog.'
    send_mail('Blog app', message, EMAIL_HOST_USER, receivers, fail_silently=False)
    return True
