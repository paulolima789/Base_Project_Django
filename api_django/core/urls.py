'''
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('api/', include('api.urls')),
]
'''
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
# Documentação da API
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="Documentação da API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="suporte@prdl.shop"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
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