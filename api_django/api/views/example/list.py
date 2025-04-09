from rest_framework.generics import ListAPIView
from api.models import Example
from api.serializers import ExampleListSerializer

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsExampleAdministrador, IsExamplePosVendas, IsExampleVendas

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema

class ExampleListView(ListAPIView):
    """Lista todos os registros de Example."""
    queryset = Example.objects.all()
    serializer_class = ExampleListSerializer
    permission_classes = [IsAuthenticated, IsExampleVendas, IsExamplePosVendas, IsExampleAdministrador]

    @swagger_auto_schema(
        operation_description="Lista todos os registros de Example.",
        responses={200: ExampleListSerializer(many=True)},
        operation_id="example_list",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)