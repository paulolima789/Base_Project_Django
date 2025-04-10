from rest_framework.generics import ListAPIView
from api.models import Example
from api.serializers import ExampleListSerializer
# paginations
from rest_framework.pagination import PageNumberPagination

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsExampleAdministrador, IsExamplePosVendas, IsExampleVendas

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema


class CustomPagination(PageNumberPagination):
    page_size = 20  # Número de itens por página
    page_size_query_param = 'page_size'  # permite o uso de ?page_size=20 na URL
    max_page_size = 100  # limite máximo

class ExampleListView(ListAPIView):
    """Lista todos os registros de Example."""
    queryset = Example.objects.all()
    serializer_class = ExampleListSerializer
    permission_classes = [IsAuthenticated, IsExampleVendas, IsExamplePosVendas, IsExampleAdministrador]
    pagination_class = CustomPagination  # 👈 Aqui tá a mágica

    @swagger_auto_schema(
        operation_description="Lista todos os registros de Example.",
        responses={200: ExampleListSerializer(many=True)},
        operation_id="example_list",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)