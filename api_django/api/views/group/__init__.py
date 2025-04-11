# api/views/group/__init__.py

from .create import GroupCreateView
from .list import GroupListView
from .detail import GroupDetailView
from .update import GroupUpdateView
from .delete import GroupDeleteView

__all__ = [
    "GroupCreateView",
    "GroupListView",
    "GroupDetailView",
    "GroupUpdateView",
    "GroupDeleteView",
]
