from rest_framework.permissions import BasePermission

# Define custom permissions for different user groups
# example: IsUser, IsAdmin, IsExample

class IsExample(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.groups.filter(name='Example').exists()

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='User').exists()