from rest_framework.generics import RetrieveAPIView
from api.models import CustomUser
from api.serializers import UserDetailSerializer

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsAdmin, IsUser, IsExample

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema

class UserDetailView(RetrieveAPIView):
    """Retorna os detalhes de um registro específico de User."""
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsUser | IsExample]

    @swagger_auto_schema(
        operation_description="Recupera os detalhes de um registro de User.",
        responses={200: UserDetailSerializer()},
        operation_id="user_detail",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)