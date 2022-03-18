from rest_framework import permissions


class IsAuthenticatedAndTechnical(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.is_technical:
            return True
        return False


class IsAuthenticatedAndExecutive(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.is_executive:
            return True
        return False
