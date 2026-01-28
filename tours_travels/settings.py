from pathlib import Path

from decouple import config
import dj_database_url
from . import admin_nav

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='change-me')
DEBUG = config('DEBUG', default=True, cast=bool)

allowed_hosts = config('ALLOWED_HOSTS', default='')
if allowed_hosts:
    ALLOWED_HOSTS = [host.strip() for host in allowed_hosts.split(',') if host.strip()]
else:
    ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_ckeditor_5',
    'crispy_forms',
    'import_export',
    'taggit',
    'rest_framework',
    'adminside',
    'users',
    'blog',
    'status',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tours_travels.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'tours_travels.wsgi.application'

DATABASE_URL = config('DATABASE_URL', default='')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_PROVIDER = config("EMAIL_PROVIDER", default="smtp")
DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL", default="Ziada Tours and Travel.com <info@ziadatoursandtravel.com>"
)
ADMIN_EMAIL = config("ADMIN_EMAIL", default="info@ziadatoursandtravel.com")
EXTRA_EMAIL_RECIPIENTS = config(
    "EXTRA_EMAIL_RECIPIENTS",
    default="",
).split(",")
SITE_URL = config("SITE_URL", default="http://127.0.0.1:8000")
MAILTRAP_API_TOKEN = config("MAILTRAP_API_TOKEN", default="")

EMAIL_HOST = config("EMAIL_HOST", default="smtp-relay.brevo.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "link",
            "bulletedList",
            "numberedList",
            "blockQuote",
            "|",
            "undo",
            "redo",
            "alignment",
            "outdent",
            "indent",
            "|",
            "imageUpload",
            "insertTable",
            "mediaEmbed",
            "codeBlock",
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "imageStyle:full",
                "imageStyle:side",
            ]
        },
        "table": {
            "contentToolbar": [
                "tableColumn",
                "tableRow",
                "mergeTableCells",
            ]
        },
    }
}

UNFOLD = {
    "SITE_TITLE": "Ziada Travel",
    "SITE_HEADER": "Ziada Travel Admin",
    "SITE_SUBHEADER": "Simple site control",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Travel Content",
                "items": [
                    {"title": "Packages", "link": admin_nav.adminside_package_list},
                    {"title": "Hotels", "link": admin_nav.adminside_hotel_list},
                    {"title": "Blog Posts", "link": admin_nav.blog_post_list},
                    {"title": "Blog Categories", "link": admin_nav.blog_category_list},
                ],
            },
            {
                "title": "Clients & Messages",
                "items": [
                    {"title": "Contact Inquiries", "link": admin_nav.users_contact_list},
                    {"title": "MICE Inquiries", "link": admin_nav.users_mice_list},
                    {"title": "Student Travel", "link": admin_nav.users_student_list},
                    {"title": "NGO Travel", "link": admin_nav.users_ngo_list},
                ],
            },
            {
                "title": "System Status",
                "items": [
                    {"app": "status"},
                ],
            },
            {
                "title": "Manage Users",
                "items": [
                    {"title": "Users", "link": admin_nav.auth_user_list},
                    {"title": "Groups", "link": admin_nav.auth_group_list},
                ],
            },
        ],
    },
}
