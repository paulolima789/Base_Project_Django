# Docker — compose e comandos úteis

Serviços principais (definidos em `docker-compose.yml`):
- django — (opcional) app container
- psql — PostgreSQL (volume: `database_volume`)
- redis — cache / broker
- mailhog — MailHog (SMTP 1025 / UI 8025)

Comandos úteis
- Subir apenas DB e MailHog:
  ```bash
  docker compose -f docker-compose.yml up -d psql redis mailhog
  ```
- Parar e remover containers e volumes do compose:
  ```bash
  docker compose -f docker-compose.yml down --volumes --remove-orphans
  ```
- Reset completo (dev — apaga dados):
  ```bash
  make docker-reset
  ```
- Limpeza agressiva (cache, imagens, build):
  ```bash
  make docker-clean
  ```

Volumes
- Se `docker volume ls` mostrar volumes externos ou com prefixo diferente, remova manualmente:
  ```bash
  docker volume rm <nome_volume>
  docker volume prune -f
  ```