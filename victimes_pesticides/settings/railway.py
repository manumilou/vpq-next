"""
Railway-specific Django settings for victimes_pesticides project.
"""

from .base import *
import os
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Railway provides the domain, but also allow custom domains
ALLOWED_HOSTS = [
    '.railway.app',
    'victimespesticidesquebec.org',
    'www.victimespesticidesquebec.org',
    os.environ.get('RAILWAY_STATIC_URL', '').replace('https://', '').replace('http://', ''),
]

# Remove empty strings
ALLOWED_HOSTS = [h for h in ALLOWED_HOSTS if h]

# CSRF trusted origins for Railway
CSRF_TRUSTED_ORIGINS = [
    'https://vpq-next-production.up.railway.app',
    'https://*.railway.app',
    'https://victimespesticidesquebec.org',
    'https://www.victimespesticidesquebec.org',
]

# Database - Railway provides DATABASE_URL automatically
# https://docs.railway.app/databases/postgresql
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files (CSS, JavaScript, Images)
# WhiteNoise for efficient static file serving
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Insert WhiteNoise middleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Use WhiteNoise's compressed manifest storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (user uploads)
# For production, consider using Railway Volumes or external storage (S3, DigitalOcean Spaces)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Security settings
# Temporarily disable SSL redirect for initial deployment debugging
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'wagtail': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Wagtail settings
WAGTAIL_SITE_NAME = 'Victimes des Pesticides du Québec'
WAGTAILADMIN_BASE_URL = os.environ.get(
    'WAGTAILADMIN_BASE_URL',
    os.environ.get('RAILWAY_STATIC_URL', 'https://vpq.railway.app')
)

# Trust Railway's proxy headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Email configuration (optional - configure when needed)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@victimespesticidesquebec.org')
