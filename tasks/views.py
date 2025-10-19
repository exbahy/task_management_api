from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateTimeFromToRangeFilter, CharFilter
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from .models import Task, TaskAssignment
from .serializers import TaskSerializer, TaskAssignmentSerializer, UserSerializer
from .permissions import IsCreatorOrReadOnly, IsSelfOrAdmin

User = get_user_model()


# ------------------------------
# 🔍 Filtering for Tasks
# ------------------------------
class TaskFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains')
    due_date = DateTimeFromToRangeFilter(field_name='due_date')
    status = CharFilter(field_name='status', lookup_expr='iexact')

    class Meta:
        model = Task
        fields = ['title', 'due_date', 'status']


# ------------------------------
# 📄 Pagination
# ------------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# ------------------------------
# 📝 Task Management
# ------------------------------
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('due_date')
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'created_at']
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        upcoming = self.request.query_params.get('upcoming')
        if upcoming and upcoming.lower() in ['1', 'true', 'yes']:
            qs = qs.filter(due_date__gt=timezone.now())
        return qs

    # ------------------------------
    # POST /tasks/{id}/assign/
    # ------------------------------
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def assign(self, request, pk=None):
        task = self.get_object()
        user = request.user

        # Prevent duplicate assignment
        existing = TaskAssignment.objects.filter(user=user, task=task).first()
        if existing:
            return Response({
                "detail": "You are already assigned to this task.",
                "status": existing.status
            }, status=status.HTTP_200_OK)

        assignment = TaskAssignment.objects.create(
            user=user, task=task, status=TaskAssignment.STATUS_ASSIGNED
        )
        serializer = TaskAssignmentSerializer(assignment)
        return Response({"detail": "Task assigned successfully.", "assignment": serializer.data}, status=status.HTTP_201_CREATED)

    # ------------------------------
    # DELETE /tasks/{id}/unassign/
    # ------------------------------
    @action(detail=True, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def unassign(self, request, pk=None):
        task = self.get_object()
        user = request.user

        assignment = TaskAssignment.objects.filter(user=user, task=task).first()
        if not assignment:
            return Response({"detail": "You are not assigned to this task."}, status=status.HTTP_404_NOT_FOUND)

        assignment.delete()
        return Response({"detail": "Unassigned successfully."}, status=status.HTTP_200_OK)


# ------------------------------
# 🧾 Task Assignment List (User-based)
# ------------------------------
class TaskAssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TaskAssignment.objects.select_related('user', 'task').all().order_by('-created_at')
    serializer_class = TaskAssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs


# ------------------------------
# 👤 User Management
# ------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':  # signup allowed
            return [AllowAny()]
        return [IsAuthenticated(), IsSelfOrAdmin()]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        user = self.get_object()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()
        serializer.save()