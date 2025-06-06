"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR.parent / 'data' / 'web'
ENV_DIR = BASE_DIR.parent / 'dotenv_files'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# importa as variáveis de ambiente
dotenv_path = ENV_DIR / '.env'
load_dotenv(dotenv_path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')

# SECURITY WARNING: don't run with debug turned on in production!
# Default: DEBUG = True
DEBUG = bool(int(os.getenv('DEBUG',0)))

# Default: ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h.strip()
]

## CORS
# libera o acesso total para todos os domínios
CORS_ORIGIN_ALLOW_ALL = False

# libera o acesso para os domínios listados
#CORS_ALLOW_ORIGIN = [
#    'http://localhost',
#    'localhost',
#    'ws://localhost:8000'
#]
CORS_ALLOWED_ORIGINS = [
    h.strip() for h in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if h.strip()
]

# Application definition

INSTALLED_APPS = [
    # third party apps
    'daphne',
    'channels',
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # installed apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'api',
    # documentação da API
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
# Channels
ASGI_APPLICATION = 'core.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# Default: SQLite
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'change-me'),
        'NAME': os.getenv('POSTGRES_DB', 'change-me'),
        'USER': os.getenv('POSTGRES_USER','change-me'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD','change-me'),
        'HOST': os.getenv('POSTGRES_HOST','psql'),
        'PORT': os.getenv('POSTGRES_PORT','change-me'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# Default: LANGUAGE_CODE = 'pt-br'
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'pt-br')
# Default: TIME_ZONE = 'America/Sao_Paulo'
TIME_ZONE = os.getenv('TIME_ZONE', 'America/Sao_Paulo')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
# /data/web/static
STATIC_ROOT = DATA_DIR / 'staticfiles'

#STATICFILES_DIRS = [
#    DATA_DIR / 'static',  # Arquivos estáticos adicionais durante o desenvolvimento
#]
# Configuração adicional para servir arquivos estáticos durante o desenvolvimento
#if DEBUG:
#    STATICFILES_DIRS.append(os.path.join(DATA_DIR, 'static'))

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# arquivos
MEDIA_URL = '/media/'
# /data/web/media
MEDIA_ROOT = DATA_DIR / 'media'

#Define o modelo de user padrão que será utilizado
AUTH_USER_MODEL = 'api.CustomUser'

#autenticação
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,  # Número de itens por página
    # Outros ajustes do DRF, como permissões, etc.
}
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
# configuração do Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # Tempo de expiração do Access Token (15 minutos)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Tempo de expiração do Refresh Token (7 dias)
    'ROTATE_REFRESH_TOKENS': False,  # Se False, o refresh token não será invalidado ao gerar um novo
    'BLACKLIST_AFTER_ROTATION': False,  # Se False, o refresh token não será colocado em uma lista negra
    'UPDATE_LAST_LOGIN': True, # Atualiza o campo `last_login` do usuário
    'ALGORITHM': 'HS256',  # Algoritmo de assinatura
     #'SIGNING_KEY': '',  # A chave secreta usada para assinar o token se quiser separar da propria SECRET_KEY
    'AUTH_HEADER_TYPES': ('Bearer',),  # Tipo do cabeçalho de autorização
}
# Configuração do Recaptcha
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY", "seu_key_aqui")
# Configuração do Google OAuth2
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "seu_id_aqui")


# Configuração do Channels Redis (caso você use Redis para WebSockets)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}
# deploy configurations

#SECURE_SSL_REDIRECT = False  # Redireciona automaticamente as requisições HTTP para HTTPS
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Para proxies reversos
#CSRF_COOKIE_SECURE = True  # Garante que o cookie CSRF só será transmitido sobre HTTPS
#SESSION_COOKIE_SECURE = True  # Garante que o cookie da sessão seja transmitido apenas via HTTPS
APPEND_SLASH = True
'''
APPEND_SLASH = True (default)	Adiciona / no final e faz redirect se não encontrar.
APPEND_SLASH = False	Não adiciona /, responde 404 se não bater a URL exata.
'''
