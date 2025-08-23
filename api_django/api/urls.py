from django.urls import path
from .views.auth.google_login import GoogleLoginView
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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views.auth.token_with_captcha import TokenObtainPairWithCaptchaView

urlpatterns = [
    # Rota para obter o token (login)
    path('token/captcha/', TokenObtainPairWithCaptchaView.as_view(), name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/google/', GoogleLoginView.as_view(), name='google-login'),
    # Rota para renovar o token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

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

    # Groups
    path("groups/", GroupListView.as_view(), name="group-list"),
    path("groups/", GroupCreateView.as_view(), name="group-create"),
    path("groups/<int:pk>/", GroupDetailView.as_view(), name="group-detail"),
    path("groups/<int:pk>/", GroupUpdateView.as_view(), name="group-update"),
    path("groups/<int:pk>/", GroupDeleteView.as_view(), name="group-delete"),
]