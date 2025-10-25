from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from accounts.utils.email import send_custom_email
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class PasswordResetRequestView(APIView):
    @swagger_auto_schema(
        tags=["Accounts"],
        operation_description="Solicita envio de link de redefinição de senha para o e-mail informado.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email')
        }, required=['email']),
        responses={200: openapi.Response('If the email exists, a reset link was sent.')}
    )
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'email required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = user.pk
            reset_link = request.build_absolute_uri(
                reverse('accounts:password_reset_confirm', kwargs={'uid': uid, 'token': token})
            )
            send_custom_email('Redefinição de senha', 'accounts/emails/password_reset.html', {'reset_link': reset_link, 'user_name': user.name or user.email}, user.email)
        return Response({'detail': 'If the email exists, a reset link was sent.'})

class PasswordResetConfirmView(APIView):
    @swagger_auto_schema(
        tags=["Accounts"],
        operation_description="Confirma e aplica nova senha a partir do uid e token recebidos no link.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password')
        }, required=['password']),
        responses={200: openapi.Response('password reset successful'), 400: 'Bad request'}
    )
    def post(self, request, uid, token):
        password = request.data.get('password')
        if not password:
            return Response({'detail': 'password required'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(pk=uid).first()
        if not user:
            return Response({'detail': 'invalid link'}, status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, token):
            return Response({'detail': 'invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.is_social_account = False
        user.save()
        return Response({'detail': 'password reset successful'})
