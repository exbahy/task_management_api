from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserViewSet, TaskAssignmentViewSet

# Initialize DRF router
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')
router.register(r'task-assignments', TaskAssignmentViewSet, basename='task-assignment')

urlpatterns = [
    # All API endpoints start with /api/
    path('api/', include(router.urls)),
]
