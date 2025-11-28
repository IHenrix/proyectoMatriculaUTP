"""
Configuración de Django para PRODUCCIÓN en Azure
Extiende settings.py base y sobrescribe configuraciones específicas de producción
"""

from .settings import *
import os

# ==============================================================================
# SECURITY SETTINGS - PRODUCCIÓN
# ==============================================================================

# DEBUG DEBE SER FALSE EN PRODUCCIÓN
DEBUG = False

# Permitir hosts de Azure App Service
# Formato: tu-app.azurewebsites.net
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Secret Key desde Azure Key Vault o Variables de Entorno
SECRET_KEY = os.environ.get('SECRET_KEY')

# Configuración de seguridad HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True


# ==============================================================================
# DATABASE CONFIGURATION - AZURE DATABASE FOR MYSQL
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'ssl': {
                'ca': os.environ.get('MYSQL_SSL_CA', None),  # Certificado SSL de Azure
            }
        }
    }
}


# ==============================================================================
# STATIC FILES - AZURE BLOB STORAGE (OPCIONAL)
# ==============================================================================

# Opción 1: Usar WhiteNoise (más simple, archivos servidos desde App Service)
# Ya configurado en settings.py base
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Opción 2: Usar Azure Blob Storage (recomendado para producción grande)
# Descomenta estas líneas si prefieres usar Blob Storage:

# INSTALLED_APPS += ['storages']

# AZURE_ACCOUNT_NAME = os.environ.get('AZURE_STORAGE_ACCOUNT_NAME')
# AZURE_ACCOUNT_KEY = os.environ.get('AZURE_STORAGE_ACCOUNT_KEY')
# AZURE_CONTAINER = os.environ.get('AZURE_STORAGE_CONTAINER_NAME', 'static')

# DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
# STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'

# AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
# STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/'


# ==============================================================================
# LOGGING - AZURE APPLICATION INSIGHTS
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/LogFiles/django_errors.log',  # Ruta en Azure App Service
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'academic_system': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# ==============================================================================
# APPLICATION INSIGHTS (OPCIONAL - Para monitoreo avanzado)
# ==============================================================================

# Descomenta si instalaste opencensus-ext-azure
# INSTRUMENTATION_KEY = os.environ.get('APPINSIGHTS_INSTRUMENTATION_KEY')

# if INSTRUMENTATION_KEY:
#     MIDDLEWARE += ['opencensus.ext.django.middleware.OpencensusMiddleware']

#     OPENCENSUS = {
#         'TRACE': {
#             'SAMPLER': 'opencensus.trace.samplers.ProbabilitySampler(rate=1.0)',
#             'EXPORTER': f'''opencensus.ext.azure.trace_exporter.AzureExporter(
#                 connection_string="InstrumentationKey={INSTRUMENTATION_KEY}"
#             )''',
#         }
#     }


# ==============================================================================
# CORS (Si necesitas llamadas desde frontend separado)
# ==============================================================================

# INSTALLED_APPS += ['corsheaders']
# MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

# CORS_ALLOWED_ORIGINS = [
#     "https://tu-frontend.azurewebsites.net",
# ]


# ==============================================================================
# EMAIL CONFIGURATION (Opcional - para notificaciones)
# ==============================================================================

# Usando Azure Communication Services o SendGrid
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@utp.edu.pe')


# ==============================================================================
# CUSTOM SETTINGS - UNIVERSITY CONFIGURATION
# ==============================================================================

UNIVERSITY_NAME = os.environ.get('UNIVERSITY_NAME', 'Universidad Tecnológica del Perú')
UNIVERSITY_SHORT_NAME = os.environ.get('UNIVERSITY_SHORT_NAME', 'UTP')
