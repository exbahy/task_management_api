from django.db import models
from django.conf import settings
from django.utils import timezone


# ------------------------------
# 📝 Task Model
# ------------------------------
class Task(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'

    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Low'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_HIGH, 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # ManyToMany through TaskAssignment model
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='TaskAssignment',
        related_name='assigned_tasks',
        blank=True,
    )

    def __str__(self):
        return f"{self.title} (Due: {self.due_date.strftime('%Y-%m-%d %H:%M')})"

    @property
    def assigned_count(self):
        """Returns the number of assigned users"""
        return self.assignments.filter(status=TaskAssignment.STATUS_ASSIGNED).count()


# ------------------------------
# 🧾 Task Assignment Model
# ------------------------------
class TaskAssignment(models.Model):
    STATUS_ASSIGNED = 'assigned'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_ASSIGNED, 'Assigned'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='task_assignments'
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ASSIGNED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'task')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} -> {self.task.title} ({self.status})"