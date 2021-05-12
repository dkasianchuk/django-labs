from rest_framework.routers import DefaultRouter
from .views import CustomUserReadViewSet, OnlineUsersViewSet

router = DefaultRouter()
router.register(r'users', CustomUserReadViewSet, basename='user')
router.register(r'online', OnlineUsersViewSet, basename='online-user')

urlpatterns = router.urls
