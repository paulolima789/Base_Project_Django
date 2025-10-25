# Development — Como rodar em dev

1. Requisitos
   - Docker + Docker Compose
   - Python 3.12
   - make

2. Preparar ambiente
   - Crie symlink do .env para que o docker-compose interpolate:
     ```bash
     ln -sf ../dotenv_files/.env .env
     ```
   - Criar e ativar venv (Makefile já cuida via `make run-dev`).

3. Subir stack de desenvolvimento
   ```bash
   # sobe psql, redis e mailhog (MailHog para testar e-mails)
   make run-dev
   ```
   - Esperar os serviços iniciarem; o Makefile executa migrations, collectstatic e `seed`.

4. Testes rápidos
   - Enviar e-mail de teste (MailHog deve estar rodando em smtp:127.0.0.1:1025):
     ```bash
     ./venv/bin/python manage.py shell -c "from django.core.mail import send_mail; send_mail('Teste','Corpo','no-reply@example.com',['teste@example.com'], fail_silently=False)"
     ```
   - Abrir MailHog: http://localhost:8025

Notas
- Para executar o Django dentro do container, ajuste `POSTGRES_HOST=psql` no `.env`.
- O settings.py já carrega `dotenv_files/.env`; evite `source` do .env no Makefile.