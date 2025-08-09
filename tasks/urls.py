from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, TaskViewSet, TagViewSet, SprintViewSet, UserViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'sprints', SprintViewSet, basename='sprint')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls
