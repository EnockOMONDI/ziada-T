from .settings import *
import os
import dj_database_url

DEBUG = False

DATABASES = {
    'default': dj_database_url.parse(
        os.getenv('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

MAILTRAP_API_TOKEN = os.getenv('MAILTRAP_API_TOKEN', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', DEFAULT_FROM_EMAIL)
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', ADMIN_EMAIL)
EXTRA_EMAIL_RECIPIENTS = os.getenv('EXTRA_EMAIL_RECIPIENTS', '').split(',')
SITE_URL = os.getenv('SITE_URL', SITE_URL)

EMAIL_PROVIDER = os.getenv('EMAIL_PROVIDER', EMAIL_PROVIDER)
EMAIL_HOST = os.getenv('EMAIL_HOST', EMAIL_HOST)
EMAIL_PORT = int(os.getenv('EMAIL_PORT', EMAIL_PORT))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', str(EMAIL_USE_TLS)).lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
