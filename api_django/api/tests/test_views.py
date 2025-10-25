import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Example
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="123456")

@pytest.fixture
def auth_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return client

@pytest.fixture
def example():
    return Example.objects.create(name="Exemplo", description="Teste")

@pytest.mark.django_db
def test_create_example(auth_client):
    url = reverse("example-create")
    data = {"name": "Novo", "description": "Teste novo"}
    response = auth_client.post(url, data)
    assert response.status_code == 201
    assert response.data["name"] == "Novo"

@pytest.mark.django_db
def test_list_example(auth_client, example):
    url = reverse("example-list")
    response = auth_client.get(url)
    assert response.status_code == 200
    # aceita listagem direta ou resposta paginada {'results': [...]}
    assert isinstance(response.data, list) or ("results" in response.data and isinstance(response.data["results"], list))

@pytest.mark.django_db
def test_detail_example(auth_client, example):
    url = reverse("example-detail", kwargs={"pk": example.pk})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data["id"] == example.id

@pytest.mark.django_db
def test_partial_update_example(auth_client, example):
    url = reverse("example-update", kwargs={"pk": example.pk})
    data = {"description": "Alterado"}
    response = auth_client.patch(url, data)
    assert response.status_code == 200
    assert response.data["description"] == "Alterado"

@pytest.mark.django_db
def test_delete_example(auth_client, example):
    url = reverse("example-delete", kwargs={"pk": example.pk})
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert not Example.objects.filter(pk=example.pk).exists()

@pytest.mark.django_db
def test_create_example_requires_auth(client):
    # client sem credenciais -> deve ser 401
    url = reverse("example-create")
    resp = client.post(url, {"name": "X", "description": "Y"})
    assert resp.status_code in (401, 403)

@pytest.mark.django_db
def test_update_example_requires_auth(client, example):
    url = reverse("example-update", kwargs={"pk": example.pk})
    resp = client.patch(url, {"description": "novo"})
    assert resp.status_code in (401, 403)

@pytest.mark.django_db
def test_delete_example_requires_auth(client, example):
    url = reverse("example-delete", kwargs={"pk": example.pk})
    resp = client.delete(url)
    assert resp.status_code in (401, 403)
