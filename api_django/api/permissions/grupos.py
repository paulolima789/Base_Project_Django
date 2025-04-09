from rest_framework.permissions import BasePermission

# Define custom permissions for different user groups
# example: IsVendas, IsPosVendas, IsAdministrador

class IsExampleVendas(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Vendas').exists()

class IsExamplePosVendas(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Pós-Vendas').exists()

class IsExampleAdministrador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.groups.filter(name='Administrador').exists()