from rest_framework.generics import ListAPIView
from django.contrib.auth.models import Group
from api.serializers import GroupDeleteSerializer
# paginations
from rest_framework.pagination import PageNumberPagination

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsAdmin, IsUser, IsExample

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema


class CustomPagination(PageNumberPagination):
    page_size = 20  # Número de itens por página
    page_size_query_param = 'page_size'  # permite o uso de ?page_size=20 na URL
    max_page_size = 100  # limite máximo

class GroupListView(ListAPIView):
    """Lista todos os registros de Group."""
    queryset = Group.objects.all()
    serializer_class = GroupDeleteSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsUser | IsExample]
    pagination_class = CustomPagination  # 👈 Aqui tá a mágica

    @swagger_auto_schema(
        operation_description="Lista todos os registros de Group.",
        responses={200: GroupDeleteSerializer(many=True)},
        operation_id="group_list",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)