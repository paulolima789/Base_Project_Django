# API — documentação e testes

Endpoints de documentação (dependendo da sua configuração):
- Swagger UI (drf-yasg): `/swagger/` ou `/documentation/`
- Schema (OpenAPI JSON/YAML): `/swagger.json` ou `/swagger.yaml`
- Redoc: `/redoc/`
- Spectacular (se usado): `/api/schema/`, `/api/schema/swagger-ui/`

Problemas comuns
- "TemplateDoesNotExist drf-yasg/swagger-ui.html": adicione `drf_yasg` em `INSTALLED_APPS` e instale a dependência.
- Erros ao gerar o schema: corrija serializers/views que referenciam campos inexistentes (ex.: `username` no user custom).

Agrupamento por CRUD
- Use `@swagger_auto_schema(tags=["Users"])` ou `@method_decorator` para agrupar endpoints por tag no Swagger.

Como inspecionar rotas no Django:
```bash
python - <<'PY'
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','core.settings')
django.setup()
from django.urls import get_resolver
for p in get_resolver().url_patterns:
    print(p.pattern, getattr(p,'name',None))
PY
```