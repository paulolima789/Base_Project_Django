import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from api.models import Example

User = get_user_model()

@pytest.fixture
def admin_user(db):
    u = User.objects.create_user(email="admin@example.test", password="adminpass")
    u.is_staff = True
    u.is_superuser = True
    u.save()
    for name in ("Admin", "User", "Example"):
        grp, _ = Group.objects.get_or_create(name=name)
        u.groups.add(grp)
    return u

@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    refresh = RefreshToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client

@pytest.fixture
def regular_user(db):
    return User.objects.create_user(email="regular@example.test", password="regularpass")

@pytest.fixture
def regular_client(regular_user):
    client = APIClient()
    refresh = RefreshToken.for_user(regular_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
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
    assert isinstance(response.data, list) or ("results" in response.data)

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
