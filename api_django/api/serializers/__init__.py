# api/serializers/__init__.py

from .example import (
    ExampleCreateSerializer,
    ExampleUpdateSerializer,
    ExampleListSerializer,
    ExampleDetailSerializer,
    ExampleDeleteSerializer
)

from .user import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserDeleteSerializer
)

from .group import (
    GroupCreateSerializer,
    GroupUpdateSerializer,
    GroupListSerializer,
    GroupDetailSerializer,
    GroupDeleteSerializer
)

from .auth import (
    TokenObtainPairWithCaptchaSerializer,
)