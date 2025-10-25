import os
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings

API_PUBLIC_URL = os.getenv('API_PUBLIC_URL', getattr(settings, 'API_PUBLIC_URL', None))

schema_view = get_schema_view(
    openapi.Info(
        title="Base_Project_Django API",
        default_version='v1',
        description="API docs",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=API_PUBLIC_URL
)

urlpatterns = [
    # panel admin
    path('admin/', admin.site.urls),
    # auth urls
    path('auth/', include('accounts.urls'), name='auth'),
    # api urls
    path('api/', include('api.urls'), name='api'),
    # Documentação da API
    path('documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )