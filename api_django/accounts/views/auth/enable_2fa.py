from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import pyotp
import qrcode
import io
import base64
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class Enable2FAView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Accounts"],
        operation_description="Gera secret TOTP e QR code para 2FA (usuário autenticado).",
        responses={200: openapi.Response('OK')}
    )
    def post(self, request):
        user = request.user
        secret = pyotp.random_base32()
        user.totp_secret = secret
        user.save()
        otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=user.email, issuer_name='MinhaApp')
        img = qrcode.make(otp_uri)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return Response({'otp_uri': otp_uri, 'qr_code_base64': b64})

class Verify2FAView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Accounts"],
        operation_description="Verifica token TOTP para habilitar 2FA.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'code': openapi.Schema(type=openapi.TYPE_STRING)
        }),
        responses={200: openapi.Response('OK'), 400: 'Bad request'}
    )
    def post(self, request):
        code = request.data.get('code')
        user = request.user
        if not user.totp_secret:
            return Response({'detail': '2FA not enabled'}, status=400)
        totp = pyotp.TOTP(user.totp_secret)
        if totp.verify(code):
            return Response({'detail': '2FA verified'})
        return Response({'detail': 'Invalid code'}, status=400)
