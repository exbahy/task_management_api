from rest_framework.permissions import BasePermission, SAFE_METHODS


# ------------------------------
# 👤 Only task creator (owner) or staff can edit/delete
# ------------------------------
class IsCreatorOrReadOnly(BasePermission):
    """
    Custom permission to allow only the task creator or admin/staff
    to edit or delete the task.
    """

    def has_object_permission(self, request, view, obj):
        # Read-only requests are allowed for any user
        if request.method in SAFE_METHODS:
            return True
        # Write permissions only for creator or staff
        return obj.creator == request.user or request.user.is_staff


# ------------------------------
# 👤 Only self or admin can view/edit user
# ------------------------------
class IsSelfOrAdmin(BasePermission):
    """
    Users can view/edit their own data, or admins can access all users.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can access anything
        if request.user.is_staff:
            return True
        # Otherwise, only allow user to access their own record
        return obj == request.user


# ------------------------------
# 📝 Only assigned user or creator can view/edit task assignment
# ------------------------------
class IsAssignedOrCreatorOrAdmin(BasePermission):
    """
    Allow task assignee, task creator, or admin to view/edit a task assignment.
    """

    def has_object_permission(self, request, view, obj):
        # Admins can access anything
        if request.user.is_staff:
            return True
        # Task creator
        if obj.task.creator == request.user:
            return True
        # Assigned user
        return obj.user == request.user
