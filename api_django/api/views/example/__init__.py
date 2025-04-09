# api/views/example/__init__.py

from .create import ExampleCreateView
from .list import ExampleListView
from .detail import ExampleDetailView
from .update import ExampleUpdateView
from .delete import ExampleDeleteView

__all__ = [
    "ExampleCreateView",
    "ExampleListView",
    "ExampleDetailView",
    "ExampleUpdateView",
    "ExampleDeleteView",
]
