from rest_framework.generics import UpdateAPIView
from api.models import Example
from api.serializers import ExampleUpdateSerializer

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsExampleAdministrador, IsExamplePosVendas, IsExampleVendas

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema

class ExampleUpdateView(UpdateAPIView):
    """Atualiza um registro existente de Example."""
    queryset = Example.objects.all()
    serializer_class = ExampleUpdateSerializer
    permission_classes = [IsAuthenticated, IsExampleVendas, IsExamplePosVendas, IsExampleAdministrador]

    @swagger_auto_schema(
        operation_description="Atualiza um registro de Example.",
        responses={200: ExampleUpdateSerializer()},
        operation_id="example_update",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualiza parcialmente um registro de Example.",
        responses={200: ExampleUpdateSerializer()},
        operation_id="example_update_partial",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)