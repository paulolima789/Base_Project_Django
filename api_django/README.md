# Base_Project_Django

Projeto Django com API REST, PostgreSQL e Docker, preparado para desenvolvimento com MailHog, documentação (Swagger) e app de autenticação reutilizável (`accounts`).

Links rápidos
- Docs do projeto: ./docs/README.md
- README do app accounts: ./accounts/README.md
- Como contribuir: ./CONTRIBUTING.md

Resumo
- API prefixada em `/api/`
- Documentação interativa: `/swagger/` ou `/documentation/` (conforme configuração)
- Rodar em dev: `make run-dev` (subirá psql, redis, mailhog e iniciará app local)

## Sumário

- [Instalação](#instalação)
- [Uso](#uso)
- [Rotas da API](#rotas-da-api)
- [Executando Testes](#executando-testes)
- [Docker](#docker)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

## Instalação

1. Clone o repositório:
   ```
   git clone <repository-url>
   cd api_django
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```
   make run-dev
   ```

## Uso

Para iniciar o servidor de desenvolvimento, execute:
```
make run-dev
```

Este comando criará um ambiente virtual, instalará os pacotes necessários, aplicará as migrações do banco de dados e iniciará o servidor usando Daphne.

## Rotas da API

Todas as rotas listadas abaixo são prefixadas por `/api/` (definido em core/urls.py).

Autenticação
- POST  /api/token/captcha/       — Obter access + refresh token com captcha (TokenObtainPairWithCaptchaView)
- POST  /api/token/               — Obter access + refresh token (TokenObtainPairView)
- POST  /api/token/google/        — Login via Google (GoogleLoginView)
- POST  /api/token/refresh/       — Renovar token (TokenRefreshView)

Examples (CRUD)
- GET   /api/examples/                  — Listar exemplos (ExampleListView)
- POST  /api/examples/create/           — Criar exemplo (ExampleCreateView)
- GET   /api/examples/{pk}/             — Detalhar exemplo (ExampleDetailView)
- PUT   /api/examples/{pk}/update/      — Atualizar exemplo (ExampleUpdateView)
- PATCH /api/examples/{pk}/update/      — Atualizar parcialmente (se implementado)
- DELETE /api/examples/{pk}/delete/     — Deletar exemplo (ExampleDeleteView)

Users (CRUD)
- GET   /api/users/                     — Listar usuários (UserListView)
- POST  /api/users/create/              — Criar usuário (UserCreateView)
- GET   /api/users/{pk}/                — Detalhar usuário (UserDetailView)
- PUT   /api/users/{pk}/update/         — Atualizar usuário (UserUpdateView)
- PATCH /api/users/{pk}/update/         — Atualizar parcialmente (se implementado)
- DELETE /api/users/{pk}/delete/        — Deletar usuário (UserDeleteView)

Groups (CRUD) — observação de conflito no código
- Intenção esperada:
  - GET   /api/groups/                  — Listar grupos (GroupListView)
  - POST  /api/groups/create/           — Criar grupo (GroupCreateView)
  - GET   /api/groups/{pk}/             — Detalhar grupo (GroupDetailView)
  - PUT   /api/groups/{pk}/update/      — Atualizar grupo (GroupUpdateView)
  - DELETE /api/groups/{pk}/delete/     — Deletar grupo (GroupDeleteView)
- Observação: no arquivo api/urls.py há caminhos duplicados para `groups/` e `groups/<int:pk>/` — isso causa conflito (apenas a primeira rota definida será usada). Recomenda-se ajustar as rotas de criação/atualização/remoção para caminhos distintos (ex.: `groups/create/`, `groups/<int:pk>/update/`, `groups/<int:pk>/delete/`) como feito para `examples` e `users`.

> Observações:
> - Os métodos exatos suportados (PUT vs PATCH, etc.) dependem da implementação das views; acima são inferências padrão com base nos nomes das views.
> - Para obter a lista exata e atual das rotas com nomes e padrões, pode-se usar o comando de gerenciamento custom (se adicionado) ou inspecionar os arquivos `api/urls.py` e outras `urls.py`.

## Executando Testes

Para executar os testes automatizados, use:
```
make run-test
```

Isto executará os testes definidos no diretório `tests` usando pytest.

## Docker

Para rodar a aplicação usando Docker, execute:
```
make run-docker
```

Este comando irá buildar a imagem Docker e iniciar todos os serviços definidos em `docker-compose.yml`.

## Contribuindo

Contribuições são bem-vindas! Abra uma issue ou envie um pull request para melhorias ou correções de bugs.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.