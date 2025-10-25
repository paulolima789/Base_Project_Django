from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Accounts"],
        operation_description="Faz logout invalidando (blacklist) o refresh token informado.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'refresh': openapi.Schema(type=openapi.TYPE_STRING)
        }, required=['refresh']),
        responses={205: openapi.Response('Logout realizado com sucesso.'), 400: 'Bad request'}
    )
    def post(self, request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response({'detail': 'refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({'detail': 'Logout realizado com sucesso.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Token inválido ou erro ao invalidar.'}, status=status.HTTP_400_BAD_REQUEST)
