import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import SocialAccount
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_google_login_creates_user(monkeypatch):
    def fake_verify(token):
        return {'email': 'social@test.com', 'name': 'Social Test', 'picture': 'http://x', 'sub': '123'}
    monkeypatch.setattr('accounts.views.auth.google_login.verify_google_token', fake_verify)
    client = APIClient()
    url = reverse('accounts:google_login')
    resp = client.post(url, {'token': 'fake'})
    assert resp.status_code == 200
    data = resp.json()
    assert 'access' in data and 'refresh' in data
    assert User.objects.filter(email='social@test.com').exists()
    assert SocialAccount.objects.filter(provider='google', social_id='123').exists()
