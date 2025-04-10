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

from .auth import (
    TokenObtainPairWithCaptchaSerializer,
)