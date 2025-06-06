from rest_framework.generics import UpdateAPIView
from api.models import CustomUser
from api.serializers import UserUpdateSerializer

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsAdmin, IsUser, IsExample

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema

class UserUpdateView(UpdateAPIView):
    """Atualiza um registro existente de User."""
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsUser | IsExample]
    
    @swagger_auto_schema(
        operation_description="Atualiza um registro de User.",
        responses={200: UserUpdateSerializer()},
        operation_id="user_update",
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualiza parcialmente um registro de User.",
        responses={200: UserUpdateSerializer()},
        operation_id="user_update_partial",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)