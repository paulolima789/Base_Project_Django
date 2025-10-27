# Define alvos "PHONY" para evitar conflito com nomes de arquivos
.PHONY: help venv run-dev run-docker run-test clean gen-secret \
	docker-stop docker-start docker-restart docker-reset docker-clean \
	docker-deps-up

# --- Configuração do Projeto ---
PROJECT_DIR := .
PROJECT_NAME := api_django
VENV := $(PROJECT_DIR)/venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MANAGE := $(PY) $(PROJECT_DIR)/manage.py
ENV_FILE := $(PROJECT_DIR)/../dotenv_files/.env
API_PORT ?= 8000

# --- Detecção do Docker Compose ---
# Detecta 'docker compose' (v2) vs 'docker-compose' (v1)
# Adiciona -f e -p para garantir que todos os comandos sejam isolados para este projeto
ifeq (, $(shell command -v docker))
	# Se docker não existe, usa docker-compose legado
	DC := docker-compose -f docker-compose.yml -p $(PROJECT_NAME)
else
ifneq (, $(shell docker compose version 2>/dev/null))
	# Se docker compose (v2) existe, use-o
	DC := docker compose -f docker-compose.yml -p $(PROJECT_NAME)
else
	# Fallback para docker-compose (v1)
	DC := docker-compose -f docker-compose.yml -p $(PROJECT_NAME)
endif
endif

# --- Alvos Principais ---

help:
	@echo "Alvos disponíveis:"
	@echo ""
	@echo "--- Desenvolvimento Local (venv) ---"
	@echo "  make venv        -> Cria/atualiza o ambiente virtual e instala dependências"
	@echo "  make run-dev     -> [Recomendado] Sobe DB/Redis (Docker), espera o DB, e roda a app localmente (venv)"
	@echo "  make run-test    -> Roda os testes (pytest) no ambiente local (venv)"
	@echo "  make clean       -> Remove o ambiente virtual local (./venv)"
	@echo "  make gen-secret  -> Gera e IMPRIME um SECRET_KEY novo no terminal"
	@echo ""
	@echo "--- Gerenciamento Docker (stack completa) ---"
	@echo "  make run-docker  -> Sobe toda a stack via docker-compose (build + up -d)"
	@echo "  make docker-stop   -> Para os containers do projeto"
	@echo "  make docker-start  -> Inicia os containers parados do projeto"
	@echo "  make docker-restart-> Reinicia os containers do projeto (aplica mudanças no compose.yml)"
	@echo "  make docker-reset  -> [PERDE DADOS] Para, remove containers E VOLUMES (banco de dados, etc)"
	@echo "  make docker-clean  -> [PERDE TUDO] Para, remove containers, VOLUMES E IMAGENS (força re-download/rebuild)"

venv:
	test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install --no-cache-dir -r requirements.txt

# run-dev: Sobe dependências (docker) e roda app (local)
# 1. 'venv' garante que as dependências python estão instaladas
# 2. 'docker-deps-up' SOBE e ESPERA o banco de dados e o redis
# 3. O resto do comando (migrate, daphne) só roda DEPOIS que o 'docker-deps-up' terminar.
run-dev: venv docker-deps-up
	@echo "📦 Carregando variáveis de ambiente e aplicando migrations..."
	@set -o allexport; \
	if [ -f $(ENV_FILE) ]; then . $(ENV_FILE); fi; \
	set +o allexport; \
	\
	$(MANAGE) makemigrations accounts --noinput; \
	$(MANAGE) makemigrations --noinput; \
	$(MANAGE) migrate --noinput; \
	$(MANAGE) collectstatic --noinput; \
	$(MANAGE) seed; \
	\
	@echo "🌐 Iniciando Daphne localmente na porta $(API_PORT)... (Ctrl+C para parar)"; \
	export DJANGO_SETTINGS_MODULE=core.settings; \
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

# --- Alvo Auxiliar para Esperar o DB ---

# NOVO ALVO: Sobe os serviços de dependência (DB, Redis) E ESPERA por eles
docker-deps-up:
	@echo "🚀 Subindo PostgreSQL, Redis e MailHog via Docker Compose..."
	$(DC) up -d psql redis mailhog

	# O '@' SÓ VAI AQUI, no início de todo o bloco de script
	@echo "📦 Carregando variáveis de ambiente para verificação do DB..."
	@set -o allexport; \
	if [ -f $(ENV_FILE) ]; then . $(ENV_FILE); fi; \
	set +o allexport; \
	\
	echo "⏳ Aguardando PostgreSQL ficar pronto (verificação: pg_isready)..."; \
	count=0; \
	while ! $(DC) exec -T psql pg_isready -U $${POSTGRES_USER} -h psql -q 2>/dev/null; do \
		count=$$((count+1)); \
		if [ $$count -gt 30 ]; then \
			echo "❌ PostgreSQL falhou em iniciar após 30 segundos."; \
			echo "Verifique o .env e os logs: '$(DC) logs psql'"; \
			exit 1; \
		fi; \
		echo "  (tentativa $$count/30) Aguardando..."; \
		sleep 1; \
	done; \
	echo "✅ PostgreSQL está pronto para conexões!"


# --- Comandos Docker Refatorados ---

# Para apenas parar os containers do projeto (não remove nada)
docker-stop:
	@echo "Parando containers do projeto '$(PROJECT_NAME)' (docker compose stop)..."
	$(DC) stop

# Inicia containers existentes do projeto (não reconstrói)
docker-start:
	@echo "Iniciando containers existentes do projeto '$(PROJECT_NAME)' (docker compose start)..."
	$(DC) start

# RESTART LEVE:
# Reinicia os serviços. Ideal para aplicar mudanças no docker-compose.yml sem forçar rebuild.
docker-restart:
	@echo "Reiniciando serviços do projeto '$(PROJECT_NAME)' (up -d --no-build)..."
	$(DC) up -d --no-build

# RESET DE DADOS:
# Para e remove containers E VOLUMES. Mantém as imagens.
# Útil quando você quer começar com um banco de dados limpo, mas sem re-baixar/re-construir imagens.
docker-reset:
	@echo "Resetando containers e volumes do projeto '$(PROJECT_NAME)' (down --volumes)..."
	$(DC) down --volumes --remove-orphans

# CLEAN COMPLETO:
# Para e remove containers, volumes E TODAS AS IMAGENS usadas pelo projeto (locais e baixadas).
# Força o re-download (postgres, redis) e o re-build (django) na próxima execução.
docker-clean:
	@echo "Limpando TUDO (Containers, Volumes e Imagens) do projeto '$(PROJECT_NAME)' (down --volumes --rmi all)..."
	$(DC) down --volumes --rmi all --remove-orphans