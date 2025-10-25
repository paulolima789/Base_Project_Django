from django.urls import path

from api.views.example import (
    ExampleListView,
    ExampleCreateView,
    ExampleDetailView,
    ExampleUpdateView,
    ExampleDeleteView,
)
from api.views.user import (
    UserListView,
    UserCreateView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,
)
from api.views.group import (
    GroupListView,
    GroupCreateView,
    GroupDetailView,
    GroupUpdateView,
    GroupDeleteView,
)

urlpatterns = [
    # Exemplos de CRUD
    path("examples/", ExampleListView.as_view(), name="example-list"),
    path("examples/create/", ExampleCreateView.as_view(), name="example-create"),
    path("examples/<int:pk>/", ExampleDetailView.as_view(), name="example-detail"),
    path("examples/<int:pk>/update/", ExampleUpdateView.as_view(), name="example-update"),
    path("examples/<int:pk>/delete/", ExampleDeleteView.as_view(), name="example-delete"),

    # Users
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user-delete"),

    # Groups (paths distintos para evitar sobrescrita)
    path("groups/", GroupListView.as_view(), name="group-list"),
    path("groups/create/", GroupCreateView.as_view(), name="group-create"),
    path("groups/<int:pk>/", GroupDetailView.as_view(), name="group-detail"),
    path("groups/<int:pk>/update/", GroupUpdateView.as_view(), name="group-update"),
    path("groups/<int:pk>/delete/", GroupDeleteView.as_view(), name="group-delete"),
]