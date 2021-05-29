from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, ActivitiesViewSet, FollowEmailViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('emails/', FollowEmailViewSet.as_view()),
    path('activities/', ActivitiesViewSet.as_view())
]
