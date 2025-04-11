from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth.models import Group
import os

User = get_user_model()

class GoogleLoginView(APIView):
    def post(self, request):
        id_token_google = request.data.get("id_token")

        if not id_token_google:
            return Response({"error": "ID Token não fornecido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Valida com o Google
            idinfo = id_token.verify_oauth2_token(
                id_token_google,
                google_requests.Request(),
                audience=os.getenv('GOOGLE_CLIENT_ID')  # ou settings.GOOGLE_CLIENT_ID
            )

            email = idinfo.get("email")
            name = idinfo.get("name")

            if not email:
                return Response({"error": "Email não encontrado no token"}, status=status.HTTP_400_BAD_REQUEST)

            # Cria ou pega usuário
            user, created = User.objects.get_or_create(email=email, defaults={"username": email, "first_name": name})

            # ➕ Adiciona o usuário ao grupo "User" se acabou de criar
            if created:
                group, _ = Group.objects.get_or_create(name="User")
                user.groups.add(group)

            # Gera tokens JWT
            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.first_name,
                }
            })

        except ValueError:
            return Response({"error": "Token inválido ou expirado"}, status=status.HTTP_400_BAD_REQUEST)