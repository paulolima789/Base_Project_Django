from rest_framework.generics import DestroyAPIView
from api.models import Example
from api.serializers import ExampleDeleteSerializer

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsExampleAdministrador, IsExamplePosVendas, IsExampleVendas

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema

class ExampleDeleteView(DestroyAPIView):
    """Remove um registro específico de Example."""
    queryset = Example.objects.all()
    serializer_class = ExampleDeleteSerializer
    permission_classes = [IsAuthenticated, IsExampleVendas, IsExamplePosVendas, IsExampleAdministrador]

    @swagger_auto_schema(
        operation_description="Remove um registro de Example.",
        responses={204: "No Content"},
        operation_id="example_delete",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)