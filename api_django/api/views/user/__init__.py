# api/views/User/__init__.py

from .create import UserCreateView
from .list import UserListView
from .detail import UserDetailView
from .update import UserUpdateView
from .delete import UserDeleteView

__all__ = [
    "UserCreateView",
    "UserListView",
    "UserDetailView",
    "UserUpdateView",
    "UserDeleteView",
]
