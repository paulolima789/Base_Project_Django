import requests
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from django.conf import settings



from drf_spectacular.utils import extend_schema, OpenApiExample

from api.serializers.auth.authSerializers import TokenObtainPairWithCaptchaSerializer



@extend_schema(
    request=TokenObtainPairWithCaptchaSerializer,
    responses={200: TokenObtainPairWithCaptchaSerializer},
    examples=[
        OpenApiExample(
            "Exemplo de login com CAPTCHA",
            summary="Autenticação com reCAPTCHA",
            description="Requisição JWT com verificação Google reCAPTCHA",
            value={
                "username": "usuario123",
                "password": "senha_segura",
                "captcha_token": "token_recaptcha_do_frontend"
            },
        )
    ]
)
class TokenObtainPairWithCaptchaView(TokenObtainPairView):
    serializer_class = TokenObtainPairWithCaptchaSerializer

    def post(self, request, *args, **kwargs):
        captcha_token = request.data.get("captcha_token")
        if not captcha_token:
            raise ValidationError({"captcha": "Captcha token é obrigatório."})

        # Verificação com Google
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": captcha_token,
            }
        )
        result = response.json()

        if not result.get("success"):
            raise ValidationError({"captcha": "Falha na verificação do CAPTCHA."})

        return super().post(request, *args, **kwargs)
