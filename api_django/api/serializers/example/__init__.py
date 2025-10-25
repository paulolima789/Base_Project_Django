# api/serializers/example/__init__.py

# importar serializers explicitamente para facilitar imports em views
from .create import ExampleCreateSerializer
from .list import ExampleListSerializer
from .detail import ExampleDetailSerializer
from .update import ExampleUpdateSerializer
from .delete import ExampleDeleteSerializer