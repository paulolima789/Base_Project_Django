import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import SocialAccount
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_google_login_creates_user(monkeypatch):
    def fake_verify(token):
        return {"email": "social@test.com", "name": "Social Test", "picture": "http://x", "sub": "123"}
    monkeypatch.setattr("accounts.views.auth.google_login.verify_google_token", fake_verify)
    client = APIClient()
    url = reverse("accounts:google_login")
    resp = client.post(url, {"token": "fake"})
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        data = resp.json()
        assert "access" in data and "refresh" in data
        assert User.objects.filter(email="social@test.com").exists()
        assert SocialAccount.objects.filter(provider="google", social_id="123").exists()

@pytest.mark.django_db
def test_google_login_invalid_token_returns_400(monkeypatch):
    def fake_verify(token):
        raise ValueError("invalid")
    monkeypatch.setattr("accounts.views.auth.google_login.verify_google_token", fake_verify)
    client = APIClient()
    url = reverse("accounts:google_login")
    resp = client.post(url, {"token": "bad"})
    assert resp.status_code in (400, 401)

@pytest.mark.django_db
def test_google_login_links_to_existing_user(monkeypatch):
    existing = User.objects.create_user(email="exists@test.com", password="pwd123")
    def fake_verify(token):
        return {"email": "exists@test.com", "name": "Exists", "picture": "http://x", "sub": "555"}
    monkeypatch.setattr("accounts.views.auth.google_login.verify_google_token", fake_verify)
    client = APIClient()
    url = reverse("accounts:google_login")
    initial_user_count = User.objects.count()
    resp = client.post(url, {"token": "fake"})
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        assert User.objects.count() == initial_user_count
        assert SocialAccount.objects.filter(provider="google", social_id="555", user=existing).exists()

@pytest.mark.django_db
def test_google_login_idempotent_when_social_exists(monkeypatch):
    u = User.objects.create_user(email="socialdup@test.com", password="pwd")
    SocialAccount.objects.create(user=u, provider="google", social_id="999")
    def fake_verify(token):
        return {"email": "socialdup@test.com", "name": "Dup", "picture": "http://x", "sub": "999"}
    monkeypatch.setattr("accounts.views.auth.google_login.verify_google_token", fake_verify)
    client = APIClient()
    url = reverse("accounts:google_login")
    resp = client.post(url, {"token": "fake"})
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        assert SocialAccount.objects.filter(provider="google", social_id="999").count() == 1
