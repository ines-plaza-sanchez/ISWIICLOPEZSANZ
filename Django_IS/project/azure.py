"""
Configuración específica para Azure App Service
Este archivo contiene todas las configuraciones necesarias para desplegar en Azure
"""

import os
from .settings import *

# DEBUG: Confirmar que se está cargando azure.py
print("🔥 CARGANDO CONFIGURACIÓN AZURE.PY 🔥")
print(f"🔥 WEBSITE_HOSTNAME: {os.environ.get('WEBSITE_HOSTNAME', 'No configurado')}")
print(f"🔥 DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE', 'No configurado')}")
print(f"🔥 SECRET_KEY (primeros 10 chars): {os.environ.get('SECRET_KEY', 'No configurado')[:10]}...")
print("🔥 AZURE.PY COMPLETAMENTE CARGADO 🔥")

# Configuración de base de datos para producción en Azure - TEMPORAL: usando SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Configuración PostgreSQL comentada temporalmente
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'djangodbprod',
#         'USER': 'rober', 
#         'PASSWORD': 'COMEmasPOLLO1',
#         'HOST': 'djangowebdbpostgre.postgres.database.azure.com',
#         'PORT': '5432',
#         'OPTIONS': {
#             'sslmode': 'require',
#         },
#     }
# }

# Configuración de seguridad para producción
# TEMPORAL: DEBUG = True para ver el error real
DEBUG = True
ALLOWED_HOSTS = [
    'rober-djangowebapp-babgd9bkfybugqfd.francecentral-01.azurewebsites.net',
    'rober-djangowebapp-babgd9bkfybugqfd.azurewebsites.net',
    '*.azurewebsites.net',
    '*.francecentral-01.azurewebsites.net',
    'localhost',
    '127.0.0.1',
    '*',  # TEMPORAL: permitir todos los hosts para diagnosticar
]

# Clave secreta de producción (debe estar en variables de entorno)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-fallback-secret-key-change-in-production-123456')

# Configuración de archivos estáticos para Azure
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Configuración de WhiteNoise para servir archivos estáticos sin colectar
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# Configuración moderna de almacenamiento estático (Django 4.2+)
# Ahora con collectstatic ejecutado, podemos usar ManifestStaticFilesStorage
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Agregar WhiteNoise middleware para servir archivos estáticos
MIDDLEWARE = [
    'relecloud.middleware.AzureDebugMiddleware',  # TEMPORAL: Debug middleware primero
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Debe ir después de SecurityMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de logging para Azure
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

# Configuración adicional para Azure
CSRF_TRUSTED_ORIGINS = [
    'https://rober-djangowebapp-babgd9bkfybugqfd.francecentral-01.azurewebsites.net',
    'https://*.azurewebsites.net',
]

# Configuración de sesiones seguras para Azure
# NOTA: Azure App Service maneja HTTPS automáticamente
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    
    # Configuración para proxy reverso de Azure
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True
    
    # NO usar SECURE_SSL_REDIRECT en Azure para evitar bucles de redirección
    SECURE_SSL_REDIRECT = False