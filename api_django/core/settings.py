# settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
from corsheaders.defaults import default_headers
from datetime import timedelta

# Base dir — usado para localizar dotenv_files/.env antes de chamar os.getenv
BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = BASE_DIR.parent / "dotenv_files" / ".env"
if DOTENV_PATH.exists():
    load_dotenv(DOTENV_PATH)
else:
    # fallback para carregar um .env no cwd, se existir
    load_dotenv()

# hosts / domínios
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CORS / CSRF
CORS_ALLOWED_ORIGINS = [x for x in os.getenv('CORS_ALLOWED_ORIGINS', ','.join(ALLOWED_HOSTS)).split(',') if x]
CORS_ALLOW_HEADERS = list(default_headers) + ['X-CSRFToken']
CSRF_TRUSTED_ORIGINS = [o for o in os.getenv('CSRF_TRUSTED_ORIGINS', ','.join(CORS_ALLOWED_ORIGINS)).split(',') if o]

# caso queira permitir tudo em dev (remova em prod)
if os.getenv('CORS_ALLOW_ALL', 'False').lower() in ('1','true','yes'):
    CORS_ALLOW_ALL_ORIGINS = True

# se o app estiver atrás de proxy TLS (nginx) — faz request.is_secure() funcionar
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Carrega .env localizado na raiz do repositório: ../dotenv_files/.env
DOTENV_PATH = BASE_DIR.parent / "dotenv_files" / ".env"
if DOTENV_PATH.exists():
    # carrega variáveis de ambiente do arquivo .env (não usar `source` no shell)
    load_dotenv(DOTENV_PATH)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')

# DEBUG: aceita "1","0","True","False"
DEBUG_RAW = os.getenv('DEBUG', '1')
DEBUG = DEBUG_RAW.lower() in ('1', 'true', 'yes', 'on')
# CSRF_TRUSTED_ORIGINS: aceita lista separada por vírgula
_csrf = os.getenv('CSRF_TRUSTED_ORIGINS', '*')
CSRF_TRUSTED_ORIGINS = [h.strip() for h in _csrf.split(',') if h.strip()]

# ALLOWED_HOSTS: aceita lista separada por vírgula
_allowed = os.getenv('ALLOWED_HOSTS', '*')
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_yasg',  # << adiciona aqui para que os templates do drf-yasg sejam encontrados
    'accounts',  # App para custom user model
    'api',  # Add your app here
    'rest_framework_simplejwt.token_blacklist',  # habilita blacklist de refresh tokens
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# Database - mapeando variáveis do .env-example
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', os.getenv('DATABASE_ENGINE', 'django.db.backends.postgresql')),
        'NAME': os.getenv('POSTGRES_DB', os.getenv('DB_NAME', 'your_db_name')),
        'USER': os.getenv('POSTGRES_USER', os.getenv('DB_USER', 'your_db_user')),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', os.getenv('DB_PASSWORD', 'your_db_password')),
        'HOST': os.getenv('POSTGRES_HOST', os.getenv('DB_HOST', 'localhost')),
        'PORT': os.getenv('POSTGRES_PORT', os.getenv('DB_PORT', '5432')),
    }
}

# Internationalization - opcionalmente sobreescrito pelo .env
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'pt-br')
TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')

USE_I18N = True
USE_L10N = True
USE_TZ = True

# CORS - simples leitura do .env
CORS_ALLOW_ALL = os.getenv('CORS_ALLOW_ALL', 'False').lower() in ('1', 'true', 'yes', 'on')
_cors_env = os.getenv('CORS_ALLOWED_ORIGINS', '').strip()
if _cors_env == '*' or CORS_ALLOW_ALL:
    CORS_ALLOW_ALL = True
    CORS_ALLOWED_ORIGINS = []
elif _cors_env:
    CORS_ALLOWED_ORIGINS = [c.strip() for c in _cors_env.split(',') if c.strip()]
else:
    CORS_ALLOWED_ORIGINS = []

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Diretório onde collectstatic grava arquivos estáticos
STATIC_ROOT = os.getenv('STATIC_ROOT', str(BASE_DIR / 'staticfiles'))

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'  # <--- substitua 'User' pelo nome real da classe encontrada

# Configurações do Django Allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
LOGIN_REDIRECT_URL = 'home'  # Substitua pela URL da sua página inicial após o login
LOGOUT_REDIRECT_URL = 'home'  # Substitua pela URL da sua página inicial após o logout

# Configurações de envio de e-mail (ler do .env se presente)
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@example.com')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', os.getenv('EMAIL_PORT', 1025)))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False').lower() in ('1', 'true', 'yes', 'on')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() in ('1', 'true', 'yes', 'on')
EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', 5))

# Django REST Framework - adicionar JWT se usar Simple JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Configurações do CORS
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'Authorization']
CORS_ALLOW_HEADERS = list(default_headers) + [
    'access-control-allow-origin',
    'access-control-allow-credentials',
]

# Força redirect para URL com '/' se faltar
APPEND_SLASH = True
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
RECAPTCHA_SECRET_KEY = os.getenv('RECAPTCHA_SECRET_KEY', '')

# Documentation Swagger e JWT 
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT token. Ex: **Bearer &lt;seu_token&gt;**',
        }
    },
    'USE_SESSION_AUTH': False,
    'DOC_EXPANSION': 'none',
    'DEFAULT_MODEL_RENDERER': 'rest_framework.renderers.BrowsableAPIRenderer',
}

# Nome do projeto usado em QR/issuer etc (lido do .env)
PROJECT_NAME = os.getenv('PROJECT_NAME', os.getenv('APP_NAME', 'Base_Project'))

# Simple JWT configurável via .env
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME_DAYS', '60'))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv('JWT_REFRESH_TOKEN_LIFETIME_DAYS', '90'))),
    'ROTATE_REFRESH_TOKENS': os.getenv('JWT_ROTATE_REFRESH_TOKENS', 'False').lower() in ('1','true','yes'),
    'BLACKLIST_AFTER_ROTATION': os.getenv('JWT_BLACKLIST_AFTER_ROTATION', 'True').lower() in ('1','true','yes'),
    'AUTH_HEADER_TYPES': tuple(os.getenv('JWT_AUTH_HEADER_TYPES', 'Bearer').split(',')),
}