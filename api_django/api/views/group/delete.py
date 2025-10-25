from rest_framework.generics import DestroyAPIView
from django.contrib.auth.models import Group
from api.serializers.group import GroupDeleteSerializer

# autenticated
from rest_framework.permissions import IsAuthenticated
from accounts.permissions.groups import IsAdmin, IsUser, IsExample

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema

class GroupDeleteView(DestroyAPIView):
    """Remove um registro específico de User."""
    queryset = Group.objects.all()
    serializer_class = GroupDeleteSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsUser | IsExample]

    @swagger_auto_schema(
        tags=["Groups"],
        operation_description="Remove um registro de Group.",
        responses={204: "No Content"},
        operation_id="group_delete",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)