from rest_framework.generics import UpdateAPIView
from django.contrib.auth.models import Group
from api.serializers import GroupDeleteSerializer

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsAdmin, IsUser, IsExample

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema

class GroupUpdateView(UpdateAPIView):
    """Atualiza um registro existente de Group."""
    queryset = Group.objects.all()
    serializer_class = GroupDeleteSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsUser | IsExample]
    
    @swagger_auto_schema(
        operation_description="Atualiza um registro de Group.",
        responses={200: GroupDeleteSerializer()},
        operation_id="group_update",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualiza parcialmente um registro de Group.",
        responses={200: GroupDeleteSerializer()},
        operation_id="group_update_partial",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)