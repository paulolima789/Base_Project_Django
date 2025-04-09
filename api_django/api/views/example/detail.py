from rest_framework.generics import RetrieveAPIView
from api.models import Example
from api.serializers import ExampleDetailSerializer

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsExampleAdministrador, IsExamplePosVendas, IsExampleVendas

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema

class ExampleDetailView(RetrieveAPIView):
    """Retorna os detalhes de um registro específico de Example."""
    queryset = Example.objects.all()
    serializer_class = ExampleDetailSerializer
    permission_classes = [IsAuthenticated, IsExampleVendas, IsExamplePosVendas, IsExampleAdministrador]

    @swagger_auto_schema(
        operation_description="Recupera os detalhes de um registro de Example.",
        responses={200: ExampleDetailSerializer()},
        operation_id="example_detail",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)