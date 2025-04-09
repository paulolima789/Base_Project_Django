import requests
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from django.conf import settings

class TokenObtainPairWithCaptchaView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        captcha_token = request.data.get("captcha_token")
        if not captcha_token:
            raise ValidationError({"captcha": "Captcha token é obrigatório."})

        # Verifica o token no Google
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

        # Se passou, executa o login normal
        return super().post(request, *args, **kwargs)