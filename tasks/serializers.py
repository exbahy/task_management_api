from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Task, TaskAssignment

User = get_user_model()


# ------------------------------
# 👤 User Serializer
# ------------------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# ------------------------------
# 🧾 Task Assignment Serializer
# ------------------------------
class TaskAssignmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    task_title = serializers.ReadOnlyField(source='task.title')
    task_due_date = serializers.ReadOnlyField(source='task.due_date')

    class Meta:
        model = TaskAssignment
        fields = [
            'id', 'user', 'task', 'task_title',
            'task_due_date', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'status', 'created_at', 'task_title', 'task_due_date']

class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_count = serializers.IntegerField(read_only=True)

    # Make due_date optional
    due_date = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date',
            'creator', 'priority', 'status', 'created_at',
            'assigned_count'
        ]
        read_only_fields = ['id', 'created_at', 'assigned_count', 'creator']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be blank.")
        return value

    def validate_due_date(self, value):
        """Ensure the due date is in the future if provided"""
        if value:
            now = timezone.now()
            if value <= now:
                raise serializers.ValidationError("Task due date must be in the future.")
        return value

    def validate(self, data):
        """Cross-field validation if start_date exists"""
        start_date = data.get('start_date')
        due_date = data.get('due_date')
        if start_date and due_date and due_date <= start_date:
            raise serializers.ValidationError("Due date must be after start date.")
        return data
