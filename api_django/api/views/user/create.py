from rest_framework.generics import CreateAPIView
from api.models import CustomUser
from api.serializers import UserCreateSerializer

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsAdmin, IsUser, IsExample

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema

class UserCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsUser | IsExample]

    @swagger_auto_schema(
        operation_description="Cria um novo User.",
        responses={201: UserCreateSerializer()},
        operation_id="user_create",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)