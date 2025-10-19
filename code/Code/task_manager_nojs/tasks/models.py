from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = 'Low'
        MEDIUM = 'Medium'
        HIGH = 'High'

    class Status(models.TextChoices):
        PENDING = 'Pending'
        COMPLETED = 'Completed'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField()
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['due_date']
