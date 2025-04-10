# 🛠️ Setup do Projeto

## 📁 Ambiente Virtual (.venv)

### Criar
```bash
py -m venv .venv
python3 -m venv .venv
```

### Ativar (no mesmo diretório)
```bash
.venv/Scripts/activate
source .venv/bin/activate
```

---

## 🧬 Git

### Configurar usuário global
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---

## 📦 Pip

### Instalação manual dos pacotes
```bash
pip install django djangorestframework django-cors-headers
```

### Gerar arquivo de dependências
```bash
pip freeze > requirements.txt
```

### Instalar a partir do `requirements.txt`
```bash
pip install -r requirements.txt
```

---

## 🌐 Django

### Criar projeto
```bash
django-admin startproject core .
```

### Criar app
```bash
py manage.py startapp api_rest
```

### Aplicar migrações no banco
```bash
python manage.py makemigrations
python manage.py migrate
```

### Rodar seed (para criar 3 tipos de login)
```bash
python manage.py seed
```

### Criar superusuário (opcional, pois já existe no banco)
```bash
python manage.py createsuperuser
```

### Rodar servidor

#### Ambiente de desenvolvimento
```bash
python manage.py runserver
```

#### Ambiente de produção (usando Daphne)
```bash
daphne -b 0.0.0.0 -p 8000 core.asgi:application
```

---

## 🐳 Docker

### Iniciar containers
```bash
docker compose up
```

### Derrubar containers
```bash
docker compose down
```

### Reconstruir containers
```bash
docker compose up --build
```

### Gerenciar imagens
```bash
docker image ls          # Listar imagens
docker image rm <id>     # Remover imagem
```

### Gerenciar containers
```bash
docker ps -a             # Listar todos os containers
docker rm <id>           # Remover container
```

### Limpar cache do Docker
```bash
docker system prune -a
```

---

## ☁️ AWS (Comandos Screen)

### Criar uma nova sessão
```bash
screen -S nome_da_sessao
```

### Desanexar da sessão
```bash
Ctrl + A, depois Ctrl + D
```

### Reanexar à sessão
```bash
screen -r nome_da_sessao
```

### Listar sessões ativas
```bash
screen -ls
```

### Finalizar a sessão
```bash
exit
```

---

> 🧾 **Dica**: Mantenha este `README.md` atualizado conforme o projeto evolui!
