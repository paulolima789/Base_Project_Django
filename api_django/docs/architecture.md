# Architecture — visão geral

Apps principais
- accounts — autenticação customizada
  - CustomUser com `email` como `USERNAME_FIELD`, campos: `is_social_account`, `totp_secret`, `name`, etc.
  - SocialAccount, password reset, 2FA (TOTP), logout com blacklist (SimpleJWT).
- api — endpoints CRUD (users, groups, examples).
- core — settings, urls, asgi/wsgi.

Fluxo de autenticação (resumido)
1. Login Social (Google): troca token do provedor por usuário local (cria se necessário).
2. Token via SimpleJWT: access/refresh; logout faz blacklist do refresh.
3. 2FA: endpoint enable gera secret e QR; verify valida código TOTP.

Banco de dados
- PostgreSQL via Docker; em dev os dados são persistidos em `database_volume`.

Documentação
- drf-yasg ou drf-spectacular para gerar OpenAPI/Swagger.