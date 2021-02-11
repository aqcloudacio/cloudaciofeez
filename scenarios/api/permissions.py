from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsSharedPractice(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user_practices = request.user.practices.all()
        if obj.practice:
            if obj.practice in user_practices:
                return True
            else:
                return False
