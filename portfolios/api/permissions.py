from rest_framework import permissions


class IsAllowedUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.allowed_users.exists():
            return request.user in obj.allowed_users.all()
        else:
            return True
