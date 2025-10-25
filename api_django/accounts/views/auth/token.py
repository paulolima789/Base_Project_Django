from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from accounts.serializers import EmailTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

# drf-yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class EmailTokenObtainPairView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        tags=["Accounts"],
        operation_description="Obter access/refresh tokens via email+senha. Envie JSON: {\"email\": \"...\", \"password\": \"...\"}.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='E-mail do usuário (campo obrigatório)'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='Senha do usuário (campo obrigatório)'),
            },
            required=['email', 'password'],
            example={"email": "user@example.com", "password": "senha123"}
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                    })
                },
                example={"refresh": "eyJ...", "access": "eyJ...", "user": {"id": 1, "email": "user@example.com", "name": "User"}}
            ),
            400: openapi.Response(description="Requisição inválida (ex.: campos faltando)"),
            401: openapi.Response(description="Credenciais inválidas")
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = EmailTokenObtainPairSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

# wrapper documentado para refresh (drf-yasg não inspeciona sempre a classe original)
class DocumentedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=["Accounts"],
        operation_description="Refresha o access token usando o refresh token. Atenção: envie SOMENTE o campo 'refresh' (o access token NÃO deve ser enviado aqui).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token recebido em /auth/token/'),
            },
            required=['refresh'],
            example={"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}
        ),
        responses={
            200: openapi.Response(
                description="Novo access token gerado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description='Novo access token'),
                    },
                    example={"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}
                )
            ),
            400: openapi.Response(description="Requisição inválida"),
            401: openapi.Response(
                description="Token inválido / expirado",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING),
                        'code': openapi.Schema(type=openapi.TYPE_STRING),
                        'messages': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                    },
                    example={
                        "detail": "Given token not valid for any token type",
                        "code": "token_not_valid",
                        "messages": [
                            {"token_class": "RefreshToken", "token_type": "refresh", "message": "Token is expired"}
                        ]
                    }
                )
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)