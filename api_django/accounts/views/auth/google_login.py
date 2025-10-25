from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from accounts.models import SocialAccount
from django.contrib.auth import get_user_model
import requests
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

def verify_google_token(token):
    try:
        resp = requests.get('https://oauth2.googleapis.com/tokeninfo', params={'id_token': token}, timeout=5)
        if resp.status_code != 200:
            return None
        return resp.json()
    except Exception:
        return None

def get_or_create_user_from_social(provider, social_id, email, name=None, avatar=None, raw_data=None):
    user = None
    if email:
        user = User.objects.filter(email=email).first()
    if not user:
        # create new user
        user = User.objects.create_user(email=email, password=None, name=name)
        user.is_social_account = True
        user.set_unusable_password()
        user.save()

    social, created = SocialAccount.objects.get_or_create(
        provider=provider,
        social_id=social_id,
        defaults={
            'user': user,
            'email': email,
            'name': name,
            'avatar': avatar,
            'verified': True,
            'raw_data': raw_data or {},
        }
    )
    if social.user != user:
        social.user = user
        social.save()
    return user

class GoogleLoginView(APIView):
    @swagger_auto_schema(
        tags=["Accounts"],
        operation_description="Loga/cria usuário via token do Google (id_token) e retorna access/refresh tokens.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING)
        }, required=['token']),
        responses={
            200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                'access': openapi.Schema(type=openapi.TYPE_STRING),
                'user': openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                })
            }),
            400: 'Bad request'
        }
    )
    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'detail': 'token required'}, status=status.HTTP_400_BAD_REQUEST)

        idinfo = verify_google_token(token)
        if not idinfo:
            return Response({'detail': 'token invalido'}, status=status.HTTP_400_BAD_REQUEST)

        email = idinfo.get('email')
        name = idinfo.get('name')
        picture = idinfo.get('picture')
        sub = idinfo.get('sub')

        user = get_or_create_user_from_social(
            provider='google',
            social_id=sub,
            email=email,
            name=name,
            avatar=picture,
            raw_data=idinfo
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {'id': user.id, 'email': user.email, 'name': user.name}
        })
