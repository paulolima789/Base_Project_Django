import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(email='u@test.com', password='123456')

@pytest.fixture
def auth_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return client

@pytest.mark.django_db
def test_enable_2fa(auth_client):
    url = reverse('accounts:enable_2fa')
    resp = auth_client.post(url)
    assert resp.status_code == 200
    assert 'otp_uri' in resp.data
    assert 'qr_code_base64' in resp.data

@pytest.mark.django_db
def test_password_reset_request(client, user):
    url = reverse('accounts:password_reset')
    resp = client.post(url, {'email': user.email})
    assert resp.status_code == 200
