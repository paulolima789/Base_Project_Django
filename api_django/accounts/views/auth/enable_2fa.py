from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import pyotp
import qrcode
from io import BytesIO
import base64
import os
from django.conf import settings

class Enable2FAView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Accounts"],
        operation_description="Gera secret TOTP e QR code para 2FA (usuário autenticado).",
        responses={200: openapi.Response('OK')}
    )
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            secret = pyotp.random_base32()
            user.totp_secret = secret
            user.save()
            issuer = getattr(settings, 'PROJECT_NAME', os.environ.get('PROJECT_NAME', 'Base_Project'))
            otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
                name=getattr(user, user.USERNAME_FIELD, 'user'),
                issuer_name=issuer
            )
            img = qrcode.make(otp_uri)
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            qr_b64 = base64.b64encode(buffer.getvalue()).decode()
            return Response({"secret": secret, "qr": f"data:image/png;base64,{qr_b64}"})
        except Exception as e:
            return Response({"detail": "Erro ao gerar 2FA"}, status=500)

class Verify2FAView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Accounts"],
        operation_description="Verifica token TOTP. Envie {\"code\":\"...\"} para apenas verificar ou {\"code\":\"...\",\"password\":\"newpass\"} para alterar a senha se o código estiver correto.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'code': openapi.Schema(type=openapi.TYPE_STRING, description='Código TOTP do app autenticador'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='(opcional) nova senha a ser aplicada se o code for válido'),
        }, required=['code']),
        responses={
            200: openapi.Response(description="2FA verificado / senha alterada"),
            400: openapi.Response(description="Bad request")
        }
    )
    def post(self, request, *args, **kwargs):
        code = str(request.data.get('code', '')).strip()
        new_password = request.data.get('password')
        user = request.user

        if not getattr(user, 'totp_secret', None):
            return Response({'detail': '2FA not enabled'}, status=400)

        secret = str(user.totp_secret).strip().strip('"').strip("'")
        totp = pyotp.TOTP(secret)

        # aceita ±1 passo (tolerância para clock drift)
        if not totp.verify(code, valid_window=1):
            return Response({'detail': 'Invalid code'}, status=400)

        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password changed'}, status=200)

        return Response({'detail': '2FA verified'}, status=200)
