# accounts/permissions/groups.py
from rest_framework.permissions import BasePermission


class GroupPermission(BasePermission):
    """
    Classe base para permissões baseadas em grupos.
    Usuário precisa estar autenticado e pertencer ao grupo especificado.
    Superusuários sempre têm permissão.
    """
    group_name = None  # deve ser definido nas subclasses

    def has_permission(self, request, view):
        # Garante autenticação
        if not request.user or not request.user.is_authenticated:
            return False

        # Superuser sempre passa
        if request.user.is_superuser:
            return True

        # Verifica se o usuário pertence ao grupo (case-insensitive)
        if self.group_name:
            return request.user.groups.filter(name__iexact=self.group_name).exists()

        return False


class IsAdmin(GroupPermission):
    """Permite acesso a usuários do grupo 'Admin' ou superusuários."""
    group_name = 'Admin'


class IsUser(GroupPermission):
    """Permite acesso a usuários do grupo 'User' ou superusuários."""
    group_name = 'User'


class IsExample(GroupPermission):
    """Permite acesso a usuários do grupo 'Example' ou superusuários."""
    group_name = 'Example'
