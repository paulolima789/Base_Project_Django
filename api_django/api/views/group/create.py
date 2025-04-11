from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import Group
from api.serializers.group import GroupCreateSerializer

from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsAdmin, IsUser, IsExample  # ou outra lógica de permissão

from drf_yasg.utils import swagger_auto_schema

class GroupCreateView(CreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsUser | IsExample]

    @swagger_auto_schema(
        operation_description="Cria um novo grupo.",
        responses={201: GroupCreateSerializer()},
        operation_id="group_create",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)