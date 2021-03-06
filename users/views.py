from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import FilterSet, DjangoFilterBackend, CharFilter
from .models import CustomUser, ConnectedUsers
from .serializers import CustomUserSerializer, ConnectedUserSerializer


class CustomUsersFilter(FilterSet):
    regex = CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ('regex', )


class CustomUserReadViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows users to view existent users.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomUsersFilter


class OnlineUsersViewSet(ReadOnlyModelViewSet):
    """
    API endpoint that allows to view online users
    """
    queryset = ConnectedUsers.objects.all()
    serializer_class = ConnectedUserSerializer
    permission_classes = [IsAuthenticated]
