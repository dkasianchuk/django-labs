from django.utils.timezone import now
from django.db.models import Model, ForeignKey, DateTimeField, CASCADE, TextField, CharField
from django.contrib.auth import get_user_model


class BlogInfoMixin(Model):
    author = ForeignKey(get_user_model(), on_delete=CASCADE, related_name='created_%(class)ss')
    publish_time = DateTimeField(default=now)
    updated_time = DateTimeField(auto_now=True)
    content = TextField()

    class Meta:
        abstract = True
        ordering = ('publish_time',)


class Post(BlogInfoMixin):
    title = CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return '{}(by {} at {}).'.format(self.title, self.author, self.publish_time)


class Comment(BlogInfoMixin):
    comment_to = ForeignKey(Post, on_delete=CASCADE, null=True, blank=True, related_name='comments')
    reply_to = ForeignKey('self', on_delete=CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return 'Comment(by {} at {}).'.format(self.author, self.publish_time)
