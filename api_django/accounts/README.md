accounts - Reusable Django authentication app (v2)
================================================

Este pacote contém um app Django chamado `accounts` com:
- CustomUser (email como identificador), campo is_social_account, totp_secret.
- SocialAccount model para armazenar dados retornados por provedores sociais.
- Login social unificado (ex: Google) que:
  - vincula ao usuário existente se o email já existir, ou
  - cria um novo usuário automaticamente caso não exista.
- Password reset (email) e confirmação (link com token).
- 2FA (TOTP) endpoints: enable e verify, com QR gerado em base64.
- Logout que faz blacklist do refresh token (SimpleJWT).
- Templates de email em `accounts/templates/accounts/emails/`.
- Permissões por grupo (Admin, User, Example) em `accounts/permissions/groups.py`.
- Testes usando pytest em `accounts/tests/`.

Como usar
---------

1. Copie a pasta `accounts` para o seu projeto Django ou instale como pacote local.
2. No settings.py:
   - Adicione 'accounts' em INSTALLED_APPS.
   - Configure AUTH_USER_MODEL = 'accounts.User' antes de rodar migrations.
   - Configure e-mail: DEFAULT_FROM_EMAIL e EMAIL_BACKEND (por exemplo console.EmailBackend no dev).
   - Adicione 'rest_framework_simplejwt.token_blacklist' em INSTALLED_APPS.
   - Instale dependências: pyotp, qrcode, pillow, requests, drf-yasg (para docs).
3. Rode migrations:
   python manage.py makemigrations accounts
   python manage.py migrate
4. Seed dos grupos:
   python manage.py seed_groups
5. URLs:
   inclua nas urls do projeto:
   path('api/accounts/', include('accounts.urls'))

Endpoints principais
--------------------
- POST /api/accounts/token/google/       -> Login com token do Google (body: { "token": "..." })
- POST /api/accounts/logout/             -> Logout (body: { "refresh": "..." })
- POST /api/accounts/password/reset/     -> Request password reset (body: { "email": "..." })
- POST /api/accounts/password/reset/confirm/<uid>/<token>/ -> Reset password (body: { "password": "..." })
- POST /api/accounts/2fa/enable/         -> Enable 2FA (authenticated)
- POST /api/accounts/2fa/verify/         -> Verify 2FA code (authenticated)

Notas de segurança
------------------
- No production, verifique tokens de provedores com bibliotecas oficiais (ex: google-auth).
- Configure HTTPS, CORS e políticas de segurança.
- Proteja endpoints sensíveis com rate limiting e lockout.

Testes
------
- Rode: pytest -q

Licença
-------
Código gerado como exemplo. Ajuste para seu domínio e políticas.
