.PHONY: help venv run-dev run-docker run-test clean gen-secret docker-stop docker-clean

PROJECT_DIR := .
VENV := $(PROJECT_DIR)/venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MANAGE := $(PY) $(PROJECT_DIR)/manage.py
DC := docker compose -f docker-compose.yml
ENV_FILE := $(PROJECT_DIR)/../dotenv_files/.env
API_PORT ?= 8000

# Detecta se 'docker compose' está disponível; caso contrário usa 'docker-compose'
ifeq (, $(shell command -v docker))
DC := docker-compose -f docker-compose.yml
else
ifneq (, $(shell docker compose version 2>/dev/null))
DC := docker compose -f docker-compose.yml
else
DC := docker-compose -f docker-compose.yml
endif
endif

help:
	@echo "Alvos disponíveis:"
	@echo "	 make run-dev	  -> sobe psql e redis (docker) e roda a app localmente (venv + deps + migrations + daphne)"
	@echo "	 make run-docker  -> sobe toda a stack via docker-compose (build + up -d)"
	@echo "	 make run-test	  -> cria venv (se necessário), instala deps e executa pytest"
	@echo "	 make clean		  -> remove venv local"
	@echo "	 make gen-secret  -> gera um SECRET_KEY novo e grava em dotenv_files/.env"

venv:
	test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install --no-cache-dir -r requirements.txt

# run-dev: sobe apenas psql e redis via docker-compose e roda Django localmente (fora do docker)
run-dev: venv
	@echo "🚀 Subindo PostgreSQL e Redis via Docker Compose..."
	$(DC) up -d psql redis

	@echo "⏳ Aguardando PostgreSQL iniciar..."
	@sleep 5

	@echo "📦 Carregando variáveis de ambiente e aplicando migrations..."
	@set -o allexport; \
	if [ -f $(ENV_FILE) ]; then . $(ENV_FILE); fi; \
	set +o allexport; \
	$(MANAGE) makemigrations --noinput; \
	$(MANAGE) migrate --noinput; \
	$(MANAGE) collectstatic --noinput
	$(MANAGE) seed

	@echo "🌐 Iniciando Daphne localmente na porta $(API_PORT)... (Ctrl+C para parar)"
	@set -o allexport; \
	if [ -f $(ENV_FILE) ]; then . $(ENV_FILE); fi; \
	export DJANGO_SETTINGS_MODULE=core.settings; \
	set +o allexport; \
	$(VENV)/bin/daphne -b 0.0.0.0 -p $(API_PORT) core.asgi:application

# run-docker: sobe toda a stack (inclui django container)
run-docker:
	$(DC) up -d --build

run-test: venv
	@set -o allexport; if [ -f $(ENV_FILE) ]; then . $(ENV_FILE); fi; set +o allexport; \
	$(VENV)/bin/pytest -q

clean:
	rm -rf $(VENV)

# Gera um SECRET_KEY novo (apenas imprime no terminal)
gen-secret:
	@echo "Gerando SECRET_KEY (apenas imprimindo)..."
	@if [ -x "$(VENV)/bin/python" ]; then \
	    $(VENV)/bin/python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"; \
	else \
	    python3 -c "import secrets; print(secrets.token_urlsafe(50)[:50])"; \
	fi

# Para parar containers montados pelo docker-compose (sem remover volumes/imagens)
docker-stop:
	@echo "Parando containers (docker compose down)..."
	$(DC) down

# Para parar e limpar volumes locais, imagens construídas e containers órfãos
docker-clean:
	@echo "Parando e limpando (volumes, todas as imagens locais do compose, órfãos)..."
	$(DC) down --volumes --rmi all --remove-orphans
	@echo "Removendo imagens dangling e cache de build..."
	-docker image prune -f
	-docker builder prune -af
	@echo "Pronto."
