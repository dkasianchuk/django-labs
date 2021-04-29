from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter
from .serializers import PostSerializer, CommentSerializer
from .models import Post, Comment


class IsAuthor(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user == obj.author)


class BaseModelViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {
        'partial_update': [IsAuthor],
        'update': [IsAuthor],
        'destroy': [IsAdminUser | IsAuthor]
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            if self.action:
                action_func = getattr(self, self.action, {})
                action_func_kwargs = getattr(action_func, 'kwargs', {})
                permission_classes = action_func_kwargs.get('permission_classes')
            else:
                permission_classes = None
            return [permission() for permission in (permission_classes or self.permission_classes)]


class PostFilter(FilterSet):
    author = NumberFilter(field_name='author__id')
    username = CharFilter(field_name='author__username')

    class Meta:
        model = Post
        fields = ('username', 'author')


class PostViewSet(BaseModelViewSet):
    """
    API endpoint that allows users to create, update, view and remove posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter


class CommentFilter(FilterSet):
    author = NumberFilter(field_name='author__id')
    post = NumberFilter(field_name='comment_to__id')
    username = CharFilter(field_name='author__username')
    comment = NumberFilter(field_name='reply_to__id')

    class Meta:
        model = Comment
        fields = ('post', 'username', 'author', 'comment')


class CommentViewSet(BaseModelViewSet):
    """
    API endpoint that allows users to create, update, view and remove comments.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_class = CommentFilter
