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
    return Example.objects.create(nome="Exemplo", descricao="Teste")

@pytest.mark.django_db
def test_create_example(auth_client):
    url = reverse("examples_create")
    data = {"nome": "Novo", "descricao": "Teste novo"}
    response = auth_client.post(url, data)
    assert response.status_code == 201
    assert response.data["nome"] == "Novo"

@pytest.mark.django_db
def test_list_example(auth_client, example):
    url = reverse("example_list")
    response = auth_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, list)

@pytest.mark.django_db
def test_detail_example(auth_client, example):
    url = reverse("example_detail", kwargs={"pk": example.pk})
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data["id"] == example.id

@pytest.mark.django_db
def test_partial_update_example(auth_client, example):
    url = reverse("example_update", kwargs={"pk": example.pk})
    data = {"descricao": "Alterado"}
    response = auth_client.patch(url, data)
    assert response.status_code == 200
    assert response.data["descricao"] == "Alterado"

@pytest.mark.django_db
def test_delete_example(auth_client, example):
    url = reverse("example_delete", kwargs={"pk": example.pk})
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert not Example.objects.filter(pk=example.pk).exists()
