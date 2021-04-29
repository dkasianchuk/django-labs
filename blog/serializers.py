from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Post, Comment


def validate_post_and_parent(data):
    if key_present_p(data, 'comment_to') == key_present_p(data, 'reply_to'):
        raise ValidationError("Either 'comment_to' or 'reply_to' should be specified.")
    return True


def key_present_p(data, key):
    try:
        return bool(data[key])
    except KeyError:
        return False


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment_to', 'reply_to', 'author', 'publish_time', 'updated_time', 'content', 'replies']
        read_only_fields = ['author', 'publish_time', 'updated_time', 'replies']

    def create(self, validated_data):
        comment = Comment(**validated_data, author=self.context['request'].user)
        comment.save()
        return comment

    def validate_comment_to(self, value):
        if self.instance and value != self.instance.comment_to:
            raise ValidationError("'comment_to' should not be changed.")
        return value

    def validate_reply_to(self, value):
        if self.instance and value != self.instance.reply_to:
            raise ValidationError("'reply_to' should not be changed.")
        return value

    def validate(self, data):
        if self.context['request'].method == 'POST':
            validate_post_and_parent(data)
        return data


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'publish_time', 'updated_time', 'title', 'content', 'comments']
        read_only_fields = ['author', 'publish_time', 'updated_time', 'comments']

    def create(self, validated_data):
        post = Post(**validated_data, author=self.context['request'].user)
        post.save()
        return post
