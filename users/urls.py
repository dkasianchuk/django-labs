from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserReadViewSet

router = DefaultRouter()
router.register(r'users', CustomUserReadViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls))
]
