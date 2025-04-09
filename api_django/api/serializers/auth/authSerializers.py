from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import requests  # ou outro método que você use para validar o captcha


class TokenObtainPairWithCaptchaSerializer(TokenObtainPairSerializer):
    captcha_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        captcha_token = attrs.pop("captcha_token", None)

        # Validação do captcha (exemplo com reCAPTCHA v2/v3 do Google)
        if not self._verify_captcha(captcha_token):
            raise serializers.ValidationError("Falha na validação do CAPTCHA.")

        # Prossegue com a validação padrão do JWT
        return super().validate(attrs)

    def _verify_captcha(self, token):
        """
        Substitua essa função com sua própria lógica de validação de CAPTCHA.
        Exemplo abaixo é para reCAPTCHA do Google.
        """
        secret_key = "SUA_CHAVE_SECRETA_DO_RECAPTCHA"
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": secret_key, "response": token}
        )
        result = response.json()
        return result.get("success", False)