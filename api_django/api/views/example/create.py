from rest_framework.generics import CreateAPIView
from api.models import Example
from api.serializers import ExampleCreateSerializer

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsExampleAdministrador, IsExamplePosVendas, IsExampleVendas

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema

class ExampleCreateView(CreateAPIView):
    queryset = Example.objects.all()
    serializer_class = ExampleCreateSerializer
    permission_classes = [IsAuthenticated, IsExampleVendas, IsExamplePosVendas, IsExampleAdministrador]

    @swagger_auto_schema(
        operation_description="Cria um novo exemplo.",
        responses={201: ExampleCreateSerializer()},
        operation_id="examples_create",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)