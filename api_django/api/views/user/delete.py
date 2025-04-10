from rest_framework.generics import DestroyAPIView
from api.models import CustomUser
from api.serializers import UserDeleteSerializer

# autenticated
from rest_framework.permissions import IsAuthenticated
from api.permissions.grupos import IsAdmin, IsUser, IsExample

# from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema

class UserDeleteView(DestroyAPIView):
    """Remove um registro específico de User."""
    queryset = CustomUser.objects.all()
    serializer_class = UserDeleteSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsUser | IsExample]

    @swagger_auto_schema(
        operation_description="Remove um registro de User.",
        responses={204: "No Content"},
        operation_id="user_delete",
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)