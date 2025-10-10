import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Define o modo de execução (DEVELOPMENT / PRODUCTION / MIGRATE)
MODE = os.getenv('MODE', 'DEVELOPMENT')

# Diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações principais
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    'backend-lacasadifrango.onrender.com',
    'localhost',
    '127.0.0.1',
    'https://lacasadifrango-api.fabricadesoftware.ifc.edu.br',
]

# 🚫 Domínios confiáveis para CSRF e CORS
CSRF_TRUSTED_ORIGINS = [
    'https://lacasadifrango.vercel.app',
    'https://lacasadifrango.fabricadesoftware.ifc.edu.br',
]

# Adiciona localhost em modo de desenvolvimento
if MODE == 'DEVELOPMENT':
    CSRF_TRUSTED_ORIGINS += [
        'http://localhost:5173',
        'http://127.0.0.1:5173',
    ]

# Aplicações
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'rest_framework',
    'core',
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # deve vir logo após SessionMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuração do CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://lacasadifrango.vercel.app',
    'https://localhost:5173',
]

if MODE in ['DEVELOPMENT', 'MIGRATE']:
    CSRF_TRUSTED_ORIGINS += [
        'http://localhost:5173',
        'http://127.0.0.1:5173',
    ]
    CORS_ALLOWED_ORIGINS += [
        'http://localhost:5173',
        'http://127.0.0.1:5173',
    ]

CORS_ALLOW_CREDENTIALS = True

# URLs e Templates
ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'

# Banco de dados (Supabase PostgreSQL)
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'static/'

# Configuração de mídia e Cloudinary
MEDIA_ENDPOINT = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
FILE_UPLOAD_PERMISSIONS = 0o640

if MODE == 'DEVELOPMENT':
    MY_IP = os.getenv('MY_IP', '127.0.0.1')
    MEDIA_URL = f'http://{MY_IP}:19003/media/'
else:
    MEDIA_URL = '/media/'
    CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
    STORAGES = {
        'default': {
            'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
        },
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        },
    }

# Campo padrão de chave primária
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração do DRF Spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'LaCasaDifrango API',
    'DESCRIPTION': 'API para sistema de pedidos, pagamentos e usuários',
    'VERSION': '1.0.0',
}

# Modelo de usuário personalizado
AUTH_USER_MODEL = 'core.User'

# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "core.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'app.pagination.CustomPagination',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'PAGE_SIZE': 10,
}

# Passage ID
PASSAGE_APP_ID = os.getenv('PASSAGE_APP_ID', 'app_id')
PASSAGE_API_KEY = os.getenv('PASSAGE_API_KEY', 'api_key')

# Debug de execução
print(f'{MODE = } \n{MEDIA_URL = } \n{DATABASES = }')
