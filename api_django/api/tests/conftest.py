import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Example

User = get_user_model()

@pytest.fixture
def create_groups(db):
    """Garante que os grupos padrão existam no banco."""
    for name in ["Admin", "User", "Example"]:
        Group.objects.get_or_create(name=name)

@pytest.fixture
def user(db, create_groups):
    """Cria um usuário comum."""
    u = User.objects.create_user(email="user@example.com", password="123456")
    group = Group.objects.get(name="User")
    u.groups.add(group)
    u.save()
    return u

@pytest.fixture
def admin_user(db, create_groups):
    """Cria um usuário administrador."""
    u = User.objects.create_user(email="admin@example.com", password="adminpass")
    u.is_superuser = True
    u.is_staff = True
    u.save()
    group = Group.objects.get(name="Admin")
    u.groups.add(group)
    return u

@pytest.fixture
def example_user(db, create_groups):
    """Cria um usuário do grupo Example."""
    u = User.objects.create_user(email="example@example.com", password="examplepass")
    group = Group.objects.get(name="Example")
    u.groups.add(group)
    u.save()
    return u

@pytest.fixture
def auth_client(user):
    """Cliente autenticado como usuário comum."""
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client

@pytest.fixture
def admin_client(admin_user):
    """Cliente autenticado como admin."""
    client = APIClient()
    refresh = RefreshToken.for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client

@pytest.fixture
def example_client(example_user):
    """Cliente autenticado como Example."""
    client = APIClient()
    refresh = RefreshToken.for_user(example_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return client

@pytest.fixture
def example(db):
    """Cria um registro Example para os testes."""
    return Example.objects.create(name="Exemplo", description="Teste de exemplo")
