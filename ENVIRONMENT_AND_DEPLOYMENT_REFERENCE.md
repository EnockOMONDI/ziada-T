# Novustell Travel - Environment and Deployment Configuration Reference

This document captures the current environment settings, switching commands, and Render deployment configuration for duplication in another system. It is based on the files listed below and reflects the exact values currently stored in this repository.

Sources reviewed
- `.env`
- `.env.development`
- `.env.production`
- `.env.production.fixed`
- `.env.production.template`
- `switch_env.py`
- `render.yaml`
- `tours_travels/settings.py`
- `tours_travels/settings_prod.py`
- `README.md`

--------------------------------------------------------------------

## 1) Environment switching commands (terminal)

Primary switcher script: `switch_env.py`

- Switch to development (copies `.env.development` -> `.env`, backs up current `.env` to `.env.backup`)
  ```bash
  python switch_env.py dev
  ```
  Next steps printed by script:
  - Restart Django dev server
  - Run `python manage.py runserver 8005`
  - Access admin at `http://127.0.0.1:8005/admin/`

- Switch to production (copies `.env.production` -> `.env` if present; otherwise edits `.env` to set `DEBUG=False` and `PRODUCTION_ENVIRONMENT=True`)
  ```bash
  python switch_env.py prod
  ```
  Next steps printed by script:
  - Deploy to production server
  - Restart production services
  - Verify at `https://novustelltravel.com/admin/`

- Show current environment status (reads `.env` and checks `DEBUG=True/False` and `SITE_URL`)
  ```bash
  python switch_env.py status
  ```

Manual development setup (from README)
```bash
cp .env.development .env
# Edit .env with your configuration
```

--------------------------------------------------------------------

## 2) How Django reads environment variables

### Base settings: `tours_travels/settings.py`
- Uses `python-decouple` and `python-dotenv` to load `.env`.
- Reads these environment variables (key settings only):
  - `DEBUG`
  - `SITE_URL`
  - `DATABASE_URL` (preferred)
  - `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` (fallback)
  - `DB_CONN_MAX_AGE`, `DB_CONN_HEALTH_CHECKS`
  - `MAILTRAP_API_TOKEN`
  - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`
  - `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
  - `EMAIL_RATE_LIMIT_PER_MINUTE`, `EMAIL_RATE_LIMIT_PER_HOUR`
  - `GOOGLE_ANALYTICS_ID`, `GOOGLE_TAG_MANAGER_ID`
  - `ENABLE_ANALYTICS`, `ANALYTICS_TRACK_ADMIN`

Notes:
- `ALLOWED_HOSTS` is hardcoded as `['*']` in `settings.py` (not read from env).
- Email addresses `ADMIN_EMAIL`, `JOBS_EMAIL`, `NEWSLETTER_EMAIL` are hardcoded in `settings.py`.

### Production overrides: `tours_travels/settings_prod.py`
- Uses `os.getenv()` directly (important for Render, which injects env vars).
- Overrides/sets these from env:
  - `DATABASE_URL` (required)
  - `MAILTRAP_API_TOKEN`
  - `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`, `ADMIN_EMAIL`, `JOBS_EMAIL`, `NEWSLETTER_EMAIL`
  - `GOOGLE_ANALYTICS_ID`, `GOOGLE_TAG_MANAGER_ID`, `ANALYTICS_TRACK_ADMIN`
  - `EMAIL_RATE_LIMIT_PER_MINUTE`, `EMAIL_RATE_LIMIT_PER_HOUR`
  - `UPLOADCARE_PUBLIC_KEY`, `UPLOADCARE_SECRET_KEY`
  - `SITE_URL`, `WHATSAPP_PHONE`, `RENDER_EXTERNAL_HOSTNAME` (for ALLOWED_HOSTS)
  - `SENTRY_DSN` (optional monitoring)

Other production-only behavior in `settings_prod.py` (hardcoded, not from env):
- `DEBUG=False`
- Security: SSL redirect, HSTS, secure cookies, security headers
- CORS: strict allowed origins
- Static/Media: WhiteNoise, staticfiles storage
- Cache: database cache
- Logging: console + rotating file under `/tmp/novustell.log`
- Health check endpoint: `/health/`
- Prints environment summary on import

--------------------------------------------------------------------

## 3) Development environment file: `.env.development`

This file is a full development configuration template. It is intended to be copied to `.env` for local use.

Exact contents (current):
```dotenv
# Development Environment Configuration for Novustell Travel
# This file should be used for local development only

# Django Core Settings
DEBUG=True
SECRET_KEY=djngo-iiamysing30ochatachterxfoatensedonfgssooeyyspw--EDIGIQDFNNNWDEJJJWEDFRTCVF
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

# Database Configuration - Using Supabase for development
DATABASE_URL=postgresql://EnockOMONDI:iuXReO7TL0rs@ep-ancient-rice-27299843-pooler.eu-central-1.aws.neon.tech:5432/neondb?sslmode=require

# Alternative database configuration (if DATABASE_URL is not used)
DB_NAME=neondb
DB_USER=EnockOMONDI
DB_PASSWORD=iuXReO7TL0rs
DB_HOST=ep-ancient-rice-27299843-pooler.eu-central-1.aws.neon.tech
DB_PORT=5432
DB_CONN_MAX_AGE=600
DB_CONN_HEALTH_CHECKS=True

# Email Configuration - Mailtrap HTTP API
MAILTRAP_API_TOKEN=d766975d57a7ef1acf2f750a36247a37
EMAIL_HOST_USER=api
EMAIL_HOST_PASSWORD=d766975d57a7ef1acf2f750a36247a37
DEFAULT_FROM_EMAIL="Novustell Travel <info@novustelltravel.com>"
ADMIN_EMAIL=info@novustelltravel.com
JOBS_EMAIL=careers@novustelltravel.com
NEWSLETTER_EMAIL=news@novustelltravel.com

# Celery Configuration (Development)
CELERY_BROKER_URL=rediss://default:AWAXAAIncDI4ZTNlNjRkMDEyOWI0OTdkODI4Nzk0ZTZlMTc1ZmQxOXAyMjQ1OTk@popular-condor-24599.upstash.io:6379
CELERY_RESULT_BACKEND=rediss://default:AWAXAAIncDI4ZTNlNjRkMDEyOWI0OTdkODI4Nzk0ZTZlMTc1ZmQxOXAyMjQ1OTk@popular-condor-24599.upstash.io:6379

# Email Rate Limiting (Development)
EMAIL_RATE_LIMIT_PER_MINUTE=10
EMAIL_RATE_LIMIT_PER_HOUR=100

# Uploadcare Configuration
UPLOADCARE_PUBLIC_KEY=ee9d364d0155cae58db7
UPLOADCARE_SECRET_KEY=23d12b50d22b09097026

# Site Configuration
SITE_URL=http://127.0.0.1:8005
WHATSAPP_PHONE=+254701363551

# Security Settings (relaxed for development)
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_HTTPONLY=True

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE=5242880
DATA_UPLOAD_MAX_MEMORY_SIZE=5242880

# Logging
LOG_LEVEL=DEBUG

# Feature Flags (enabled for development testing)
ENABLE_BOOKING_NOTIFICATIONS=True
ENABLE_EMAIL_MARKETING=False
ENABLE_ANALYTICS=False
ENABLE_CHAT_SUPPORT=False
RATE_LIMIT_ENABLED=False
RATE_LIMIT_PER_MINUTE=1000

# Session Configuration
SESSION_COOKIE_AGE=86400
SESSION_EXPIRE_AT_BROWSER_CLOSE=False

# Development Tools
ENABLE_DEBUG_TOOLBAR=True
ENABLE_SILK_PROFILING=False

# Environment Indicators
PRODUCTION_ENVIRONMENT=False
STAGING_ENVIRONMENT=False
QA_ENVIRONMENT=False

# Maintenance Mode
MAINTENANCE_MODE=False

# Time Zone
TIME_ZONE=Africa/Nairobi
DEFAULT_LANGUAGE=en

# Booking Configuration
DEFAULT_BOOKING_EXPIRY_HOURS=24
MAX_BOOKING_ADULTS=50
MAX_BOOKING_CHILDREN=15
MAX_BOOKING_ROOMS=20

# Search Configuration
SEARCH_RESULTS_PER_PAGE=12
ENABLE_SEARCH_SUGGESTIONS=True

# Image Processing
IMAGE_QUALITY=85
THUMBNAIL_SIZE=300x200
HERO_IMAGE_SIZE=1920x1080

# Customer Support
SUPPORT_EMAIL=technical@novustelltravel.com
SUPPORT_PHONE=+254701363551

# Legal and Compliance
PRIVACY_POLICY_URL=/privacy-policy/
TERMS_OF_SERVICE_URL=/terms-of-service/
COOKIE_POLICY_URL=/cookie-policy/
GDPR_COMPLIANCE=True

# Development Information
DEPLOYMENT_DATE=2025-08-11
VERSION=1.0.0-dev
BUILD_NUMBER=dev
COMMIT_HASH=development

# Business Rules
MIN_BOOKING_ADVANCE_DAYS=1
MAX_BOOKING_ADVANCE_DAYS=365
CANCELLATION_DEADLINE_HOURS=48
REFUND_PROCESSING_DAYS=7

# Feature Toggles
ENABLE_GUEST_CHECKOUT=True
ENABLE_USER_REGISTRATION=True
ENABLE_SOCIAL_LOGIN=False
ENABLE_MULTI_LANGUAGE=False
ENABLE_DARK_MODE=False
ENABLE_OFFLINE_MODE=False

# Performance Settings (relaxed for development)
MAX_REQUEST_SIZE_MB=50
MAX_UPLOAD_SIZE_MB=25
MAX_SESSION_SIZE_KB=500
MAX_CACHE_SIZE_MB=1000

# Security Thresholds (relaxed for development)
MAX_LOGIN_ATTEMPTS=10
LOCKOUT_DURATION_MINUTES=5
PASSWORD_RESET_TIMEOUT_HOURS=24
SESSION_TIMEOUT_HOURS=24

# Regional Settings
DEFAULT_COUNTRY=Kenya
DEFAULT_CURRENCY=USD
SUPPORTED_CURRENCIES=USD,KES,EUR,GBP
PHONE_NUMBER_REGION=KE
CURRENCY_SYMBOL=$
DATE_FORMAT=%Y-%m-%d
TIME_FORMAT=%H:%M:%S
DATETIME_FORMAT=%Y-%m-%d %H:%M:%S

# Data Retention
DATA_RETENTION_DAYS=2555
COOKIE_CONSENT_REQUIRED=True
PRIVACY_POLICY_VERSION=1.0
TERMS_VERSION=1.0

# Business Logic
BOOKING_CONFIRMATION_DELAY_MINUTES=1
PAYMENT_TIMEOUT_MINUTES=30
SESSION_WARNING_MINUTES=5
AUTO_LOGOUT_MINUTES=120
```

--------------------------------------------------------------------

## 4) Current local environment file: `.env`

`.env` currently matches development and is used by `settings.py` via `load_dotenv()`. It is not identical to `.env.development` (notable differences are listed below).

Exact contents (current):
```dotenv
# Development Environment Configuration for Novustell Travel
# This file should be used for local development only

# Django Core Settings
DEBUG=True
SECRET_KEY=djngo-iiamysing30ochatachterxfoatensedonfgssooeyyspw--EDIGIQDFNNNWDEJJJWEDFRTCVF
ALLOWED_HOSTS=127.0.0.1,localhost,0.0.0.0

# Database Configuration - Using Supabase for development
DATABASE_URL=postgresql://EnockOMONDI:iuXReO7TL0rs@ep-ancient-rice-27299843-pooler.eu-central-1.aws.neon.tech:5432/neondb?sslmode=require

# Alternative database configuration (if DATABASE_URL is not used)
DB_NAME=neondb
DB_USER=EnockOMONDI
DB_PASSWORD=iuXReO7TL0rs
DB_HOST=ep-ancient-rice-27299843-pooler.eu-central-1.aws.neon.tech
DB_PORT=5432
DB_CONN_MAX_AGE=600
DB_CONN_HEALTH_CHECKS=True

# Email Configuration
# MAILTRAP EMAIL CONFIGURATION - CRITICAL UPDATE
EMAIL_HOST=live.smtp.mailtrap.io
EMAIL_HOST_USER=api
EMAIL_HOST_PASSWORD=d766975d57a7ef1acf2f750a36247a37
DEFAULT_FROM_EMAIL=Novustell Travel <info@novustelltravel.com>
ADMIN_EMAIL=info@novustelltravel.com
JOBS_EMAIL=careers@novustelltravel.com
NEWSLETTER_EMAIL=news@novustelltravel.com

# Uploadcare Configuration
UPLOADCARE_PUBLIC_KEY=ee9d364d0155cae58db7
UPLOADCARE_SECRET_KEY=23d12b50d22b09097026

# Site Configuration
SITE_URL=http://127.0.0.1:8005
WHATSAPP_PHONE=+254701363551

# Analytics Configuration
GOOGLE_ANALYTICS_ID=G-JV4GQKWVJL

# Security Settings (relaxed for development)
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_HTTPONLY=True

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE=5242880
DATA_UPLOAD_MAX_MEMORY_SIZE=5242880

# Logging
LOG_LEVEL=DEBUG

# Feature Flags (enabled for development testing)
ENABLE_BOOKING_NOTIFICATIONS=True
ENABLE_EMAIL_MARKETING=True
ENABLE_ANALYTICS=False
ENABLE_CHAT_SUPPORT=False
RATE_LIMIT_ENABLED=False
RATE_LIMIT_PER_MINUTE=1000

# Session Configuration
SESSION_COOKIE_AGE=86400
SESSION_EXPIRE_AT_BROWSER_CLOSE=False

# Development Tools
ENABLE_DEBUG_TOOLBAR=True
ENABLE_SILK_PROFILING=False

# Environment Indicators
PRODUCTION_ENVIRONMENT=False
STAGING_ENVIRONMENT=False
QA_ENVIRONMENT=False

# Maintenance Mode
MAINTENANCE_MODE=False

# Time Zone
TIME_ZONE=Africa/Nairobi
DEFAULT_LANGUAGE=en

# Booking Configuration
DEFAULT_BOOKING_EXPIRY_HOURS=24
MAX_BOOKING_ADULTS=50
MAX_BOOKING_CHILDREN=15
MAX_BOOKING_ROOMS=20

# Search Configuration
SEARCH_RESULTS_PER_PAGE=12
ENABLE_SEARCH_SUGGESTIONS=True

# Image Processing
IMAGE_QUALITY=85
THUMBNAIL_SIZE=300x200
HERO_IMAGE_SIZE=1920x1080

# Customer Support
SUPPORT_EMAIL=technical@novustelltravel.com
SUPPORT_PHONE=+254701363551

# Legal and Compliance
PRIVACY_POLICY_URL=/privacy-policy/
TERMS_OF_SERVICE_URL=/terms-of-service/
COOKIE_POLICY_URL=/cookie-policy/
GDPR_COMPLIANCE=True

# Development Information
DEPLOYMENT_DATE=2025-08-11
VERSION=1.0.0-dev
BUILD_NUMBER=dev
COMMIT_HASH=development

# Business Rules
MIN_BOOKING_ADVANCE_DAYS=1
MAX_BOOKING_ADVANCE_DAYS=365
CANCELLATION_DEADLINE_HOURS=48
REFUND_PROCESSING_DAYS=7

# Feature Toggles
ENABLE_GUEST_CHECKOUT=True
ENABLE_USER_REGISTRATION=True
ENABLE_SOCIAL_LOGIN=False
ENABLE_MULTI_LANGUAGE=False
ENABLE_DARK_MODE=False
ENABLE_OFFLINE_MODE=False

# Performance Settings (relaxed for development)
MAX_REQUEST_SIZE_MB=50
MAX_UPLOAD_SIZE_MB=25
MAX_SESSION_SIZE_KB=500
MAX_CACHE_SIZE_MB=1000

# Security Thresholds (relaxed for development)
MAX_LOGIN_ATTEMPTS=10
LOCKOUT_DURATION_MINUTES=5
PASSWORD_RESET_TIMEOUT_HOURS=24
SESSION_TIMEOUT_HOURS=24

# Regional Settings
DEFAULT_COUNTRY=Kenya
DEFAULT_CURRENCY=USD
SUPPORTED_CURRENCIES=USD,KES,EUR,GBP
PHONE_NUMBER_REGION=KE
CURRENCY_SYMBOL=$
DATE_FORMAT=%Y-%m-%d
TIME_FORMAT=%H:%M:%S
DATETIME_FORMAT=%Y-%m-%d %H:%M:%S

# Data Retention
DATA_RETENTION_DAYS=2555
COOKIE_CONSENT_REQUIRED=True
PRIVACY_POLICY_VERSION=1.0
TERMS_VERSION=1.0

# Business Logic
BOOKING_CONFIRMATION_DELAY_MINUTES=1
PAYMENT_TIMEOUT_MINUTES=30
SESSION_WARNING_MINUTES=5
AUTO_LOGOUT_MINUTES=120
MAILTRAP_API_TOKEN=d766975d57a7ef1acf2f750a36247a37
```

Differences vs `.env.development`
- `.env` uses SMTP-style `EMAIL_HOST=live.smtp.mailtrap.io` and also includes `MAILTRAP_API_TOKEN` at the end.
- `.env.development` includes Celery configuration and has `ENABLE_EMAIL_MARKETING=False`.

--------------------------------------------------------------------

## 5) Production environment file: `.env.production`

This file is intended for production configuration (local or non-Render deployments). On Render, these values are set via `render.yaml` and the Render dashboard.

Exact contents (current):
```dotenv
# CRITICAL FIX: Updated production environment variables
# This file contains the CORRECT email password to fix the SMTP timeout issue

# Django Core
DJANGO_SETTINGS_MODULE=tours_travels.settings_prod
SECRET_KEY=django-insecure-change-this-in-production-use-50-characters-minimum
DEBUG=False
ALLOWED_HOSTS=novustelltravel.onrender.com,.onrender.com,novustelltravel.com,www.novustelltravel.com

# Database
DATABASE_URL=postgresql://novustell_user:your_password@ep-example-123456.us-east-1.aws.neon.tech/novustell_travel?sslmode=require

# MAILTRAP HTTP API CONFIGURATION - CRITICAL UPDATE
MAILTRAP_API_TOKEN=d766975d57a7ef1acf2f750a36247a37
EMAIL_HOST_USER=api
EMAIL_HOST_PASSWORD=d766975d57a7ef1acf2f750a36247a37
DEFAULT_FROM_EMAIL="Novustell Travel <info@novustelltravel.com>"
ADMIN_EMAIL=info@novustelltravel.com
JOBS_EMAIL=careers@novustelltravel.com
NEWSLETTER_EMAIL=news@novustelltravel.com
# Analytics Configuration
GOOGLE_ANALYTICS_ID=G-JV4GQKWVJL
ENABLE_ANALYTICS=True

# Celery Configuration
CELERY_BROKER_URL=rediss://default:AWAXAAIncDI4ZTNlNjRkMDEyOWI0OTdkODI4Nzk0ZTZlMTc1ZmQxOXAyMjQ1OTk@popular-condor-24599.upstash.io:6379
CELERY_RESULT_BACKEND=rediss://default:AWAXAAIncDI4ZTNlNjRkMDEyOWI0OTdkODI4Nzk0ZTZlMTc1ZmQxOXAyMjQ1OTk@popular-condor-24599.upstash.io:6379

# Email Rate Limiting
EMAIL_RATE_LIMIT_PER_MINUTE=100
EMAIL_RATE_LIMIT_PER_HOUR=1000

# Feature Flags (enabled for development testing)
ENABLE_BOOKING_NOTIFICATIONS=True
ENABLE_EMAIL_MARKETING=True
ENABLE_ANALYTICS=True
ENABLE_CHAT_SUPPORT=True
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=1000

# Uploadcare Configuration
UPLOADCARE_PUBLIC_KEY=ee9d364d0155cae58db7
UPLOADCARE_SECRET_KEY=23d12b50d22b09097026

# Site Configuration
SITE_URL=https://novustelltravel.onrender.com
WHATSAPP_PHONE=+254701363551

# Security Settings (Production)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Performance Settings
WEB_CONCURRENCY=3
GUNICORN_TIMEOUT=120



# Additional Production Settings
USE_TZ=True
TIME_ZONE=Africa/Nairobi
LANGUAGE_CODE=en-us

# Database Connection
DB_CONN_MAX_AGE=600
DB_CONN_HEALTH_CHECKS=True

# Cache Configuration
CACHE_TIMEOUT=300

# File Upload Limits
MAX_UPLOAD_SIZE_MB=5
FILE_UPLOAD_MAX_MEMORY_SIZE=5242880

# Regional Settings
DEFAULT_COUNTRY=Kenya
DEFAULT_CURRENCY=USD
PHONE_NUMBER_REGION=KE

# Business Configuration
BOOKING_CONFIRMATION_DELAY_MINUTES=5
PAYMENT_TIMEOUT_MINUTES=30
SESSION_WARNING_MINUTES=5
AUTO_LOGOUT_MINUTES=60

# Feature Toggles
ENABLE_GUEST_CHECKOUT=True
ENABLE_USER_REGISTRATION=True
ENABLE_SOCIAL_LOGIN=False

# Performance Monitoring
PRODUCTION_ENVIRONMENT=True
QA_ENVIRONMENT=False
STAGING_ENVIRONMENT=False

# Data Retention
DATA_RETENTION_DAYS=2555
COOKIE_CONSENT_REQUIRED=True
PRIVACY_POLICY_VERSION=1.0
TERMS_VERSION=1.0

# Maintenance Settings
AUTO_UPDATE_ENABLED=False
MAINTENANCE_WINDOW_START=02:00
MAINTENANCE_WINDOW_END=04:00
MAINTENANCE_TIMEZONE=Africa/Nairobi

# Security Thresholds
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=30
PASSWORD_RESET_TIMEOUT_HOURS=24
SESSION_TIMEOUT_HOURS=24

# Business Rules
MIN_BOOKING_ADVANCE_DAYS=1
MAX_BOOKING_ADVANCE_DAYS=365
CANCELLATION_DEADLINE_HOURS=48
REFUND_PROCESSING_DAYS=7
```

Notes
- `ENABLE_ANALYTICS` appears twice (Analytics section and Feature Flags section). Both are `True`.
- Celery variables are present here, but Render configuration has Celery services commented out.

--------------------------------------------------------------------

## 6) Production backup file: `.env.production.fixed`

This is a production file labeled as a "critical fix" and is very similar to `.env.production`, but it omits some sections (analytics, celery, rate limiting, etc.).

Exact contents (current):
```dotenv
# CRITICAL FIX: Updated production environment variables
# This file contains the CORRECT email password to fix the SMTP timeout issue

# Django Core
DJANGO_SETTINGS_MODULE=tours_travels.settings_prod
SECRET_KEY=django-insecure-change-this-in-production-use-50-characters-minimum
DEBUG=False
ALLOWED_HOSTS=novustelltravel.onrender.com,.onrender.com,novustelltravel.com,www.novustelltravel.com

# Database
DATABASE_URL=postgresql://novustell_user:your_password@ep-example-123456.us-east-1.aws.neon.tech/novustell_travel?sslmode=require

# MAILTRAP HTTP API CONFIGURATION - CRITICAL UPDATE
MAILTRAP_API_TOKEN=d766975d57a7ef1acf2f750a36247a37
EMAIL_HOST_USER=api
EMAIL_HOST_PASSWORD=d766975d57a7ef1acf2f750a36247a37
DEFAULT_FROM_EMAIL=Novustell Travel <info@novustelltravel.com>
ADMIN_EMAIL=info@novustelltravel.com
JOBS_EMAIL=careers@novustelltravel.com
NEWSLETTER_EMAIL=news@novustelltravel.com

# Uploadcare Configuration
UPLOADCARE_PUBLIC_KEY=ee9d364d0155cae58db7
UPLOADCARE_SECRET_KEY=23d12b50d22b09097026

# Site Configuration
SITE_URL=https://novustelltravel.onrender.com
WHATSAPP_PHONE=+254701363551

# Security Settings (Production)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Performance Settings
WEB_CONCURRENCY=3
GUNICORN_TIMEOUT=120



# Additional Production Settings
USE_TZ=True
TIME_ZONE=Africa/Nairobi
LANGUAGE_CODE=en-us

# Database Connection
DB_CONN_MAX_AGE=600
DB_CONN_HEALTH_CHECKS=True

# Cache Configuration
CACHE_TIMEOUT=300

# File Upload Limits
MAX_UPLOAD_SIZE_MB=5
FILE_UPLOAD_MAX_MEMORY_SIZE=5242880

# Regional Settings
DEFAULT_COUNTRY=Kenya
DEFAULT_CURRENCY=USD
PHONE_NUMBER_REGION=KE

# Business Configuration
BOOKING_CONFIRMATION_DELAY_MINUTES=5
PAYMENT_TIMEOUT_MINUTES=30
SESSION_WARNING_MINUTES=5
AUTO_LOGOUT_MINUTES=60

# Feature Toggles
ENABLE_GUEST_CHECKOUT=True
ENABLE_USER_REGISTRATION=True
ENABLE_SOCIAL_LOGIN=False

# Performance Monitoring
PRODUCTION_ENVIRONMENT=True
QA_ENVIRONMENT=False
STAGING_ENVIRONMENT=False

# Data Retention
DATA_RETENTION_DAYS=2555
COOKIE_CONSENT_REQUIRED=True
PRIVACY_POLICY_VERSION=1.0
TERMS_VERSION=1.0

# Maintenance Settings
AUTO_UPDATE_ENABLED=False
MAINTENANCE_WINDOW_START=02:00
MAINTENANCE_WINDOW_END=04:00
MAINTENANCE_TIMEZONE=Africa/Nairobi

# Security Thresholds
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION_MINUTES=30
PASSWORD_RESET_TIMEOUT_HOURS=24
SESSION_TIMEOUT_HOURS=24

# Business Rules
MIN_BOOKING_ADVANCE_DAYS=1
MAX_BOOKING_ADVANCE_DAYS=365
CANCELLATION_DEADLINE_HOURS=48
REFUND_PROCESSING_DAYS=7
```

--------------------------------------------------------------------

## 7) Production template: `.env.production.template`

This is the long-form template with placeholders and optional settings. It includes many variables not currently used in `.env.production`.

Exact contents (current):
```dotenv
# Production Environment Variables for Novustell Travel
# Copy this file to .env.production and fill in the actual values

# Django Settings
DJANGO_SETTINGS_MODULE=tours_travels.settings_prod
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=novustelltravel.onrender.com,.onrender.com,novustelltravel.com,www.novustelltravel.com

# Database Configuration (NeonDB)
DATABASE_URL=postgresql://username:password@hostname:port/database_name

# Email Configuration (Mailtrap HTTP API)
MAILTRAP_API_TOKEN=d766975d57a7ef1acf2f750a36247a37
EMAIL_HOST_USER=api
EMAIL_HOST_PASSWORD=d766975d57a7ef1acf2f750a36247a37
DEFAULT_FROM_EMAIL=Novustell Travel <info@novustelltravel.com>
ADMIN_EMAIL=info@novustelltravel.com
JOBS_EMAIL=careers@novustelltravel.com
NEWSLETTER_EMAIL=news@novustelltravel.com

# Uploadcare Configuration
UPLOADCARE_PUBLIC_KEY=your-uploadcare-public-key
UPLOADCARE_SECRET_KEY=your-uploadcare-secret-key

# Site Configuration
SITE_URL=https://novustelltravel.onrender.com
WHATSAPP_PHONE=+254701363551

# Render Configuration
RENDER_EXTERNAL_HOSTNAME=novustelltravel.onrender.com
PORT=10000

# Security Settings
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Performance Settings
WEB_CONCURRENCY=3
GUNICORN_WORKERS=3
GUNICORN_TIMEOUT=120

# Monitoring (Optional)
SENTRY_DSN=your-sentry-dsn-here

# Cache Configuration
CACHE_URL=redis://localhost:6379/1

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE=5242880
DATA_UPLOAD_MAX_MEMORY_SIZE=5242880

# Logging Level
LOG_LEVEL=INFO

# Backup Configuration (Optional)
BACKUP_STORAGE_URL=s3://your-backup-bucket/
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Social Media Integration (Optional)
FACEBOOK_APP_ID=your-facebook-app-id
GOOGLE_ANALYTICS_ID=your-google-analytics-id

# Payment Gateway (Optional - for future implementation)
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret

# API Keys (Optional)
GOOGLE_MAPS_API_KEY=your-google-maps-api-key
WEATHER_API_KEY=your-weather-api-key

# Feature Flags
ENABLE_BOOKING_NOTIFICATIONS=True
ENABLE_EMAIL_MARKETING=True
ENABLE_ANALYTICS=True
ENABLE_CHAT_SUPPORT=False

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60

# Content Delivery Network (Optional)
CDN_URL=https://your-cdn-domain.com
USE_CDN=False

# Database Connection Pool
DB_CONN_MAX_AGE=600
DB_CONN_HEALTH_CHECKS=True

# Session Configuration
SESSION_COOKIE_AGE=86400
SESSION_EXPIRE_AT_BROWSER_CLOSE=False

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://novustelltravel.onrender.com,https://www.novustelltravel.com

# Content Security Policy
CSP_REPORT_URI=/csp-report/
CSP_REPORT_ONLY=False

# Health Check Configuration
HEALTH_CHECK_URL=/health/
HEALTH_CHECK_ACCESS_TOKEN=your-health-check-token

# Maintenance Mode
MAINTENANCE_MODE=False
MAINTENANCE_MESSAGE=We are currently performing scheduled maintenance. Please check back soon.

# Internationalization
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,sw
TIME_ZONE=Africa/Nairobi

# Media Storage (for production - consider AWS S3)
USE_S3_MEDIA=False
AWS_S3_CUSTOM_DOMAIN=your-cloudfront-domain.cloudfront.net

# Email Templates
EMAIL_TEMPLATE_DIR=users/templates/users/emails/
EMAIL_LOGO_URL=https://your-cdn.com/logo.png

# Booking Configuration
DEFAULT_BOOKING_EXPIRY_HOURS=24
MAX_BOOKING_ADULTS=20
MAX_BOOKING_CHILDREN=15
MAX_BOOKING_ROOMS=10

# Search Configuration
SEARCH_RESULTS_PER_PAGE=12
ENABLE_SEARCH_SUGGESTIONS=True

# Image Processing
IMAGE_QUALITY=85
THUMBNAIL_SIZE=300x200
HERO_IMAGE_SIZE=1920x1080

# Notification Settings
SLACK_WEBHOOK_URL=your-slack-webhook-url
DISCORD_WEBHOOK_URL=your-discord-webhook-url

# Backup Schedule
BACKUP_FREQUENCY=daily
BACKUP_RETENTION_DAYS=30

# Performance Monitoring
NEW_RELIC_LICENSE_KEY=your-new-relic-license-key
DATADOG_API_KEY=your-datadog-api-key

# SSL Certificate
SSL_CERT_PATH=/etc/ssl/certs/novustell.crt
SSL_KEY_PATH=/etc/ssl/private/novustell.key

# Load Balancer
USE_LOAD_BALANCER=False
LOAD_BALANCER_HEALTH_CHECK=/lb-health/

# Geographic Configuration
DEFAULT_COUNTRY=Kenya
DEFAULT_CURRENCY=USD
SUPPORTED_CURRENCIES=USD,KES,EUR,GBP

# Analytics and Tracking
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
GOOGLE_TAG_MANAGER_ID=GTM-XXXXXXX
ENABLE_ANALYTICS=True
ANALYTICS_TRACK_ADMIN=False
FACEBOOK_PIXEL_ID=your-facebook-pixel-id
HOTJAR_ID=your-hotjar-id

# Customer Support
SUPPORT_EMAIL=technical@novustelltravel.com
SUPPORT_PHONE=+254701363551
ZENDESK_SUBDOMAIN=novustell
INTERCOM_APP_ID=your-intercom-app-id

# Marketing Automation
MAILCHIMP_API_KEY=your-mailchimp-api-key
MAILCHIMP_LIST_ID=your-mailchimp-list-id
SENDGRID_API_KEY=your-sendgrid-api-key

# Legal and Compliance
PRIVACY_POLICY_URL=/privacy-policy/
TERMS_OF_SERVICE_URL=/terms-of-service/
COOKIE_POLICY_URL=/cookie-policy/
GDPR_COMPLIANCE=True

# Development and Testing
ENABLE_DEBUG_TOOLBAR=False
ENABLE_SILK_PROFILING=False
TEST_DATABASE_NAME=test_novustell_travel

# Deployment Information
DEPLOYMENT_DATE=2025-07-25
```

--------------------------------------------------------------------

## 8) Render deployment configuration: `render.yaml`

### Web service definition
- Service type: web
- Name: `novustellke`
- Runtime: Python
- Region: oregon
- Plan: starter
- Branch: `googleanalytics`
- Health check path: `/health/`
- Auto-deploy: true
- Disk mount: `novustell-disk` at `/opt/render/project/src/media` (1GB)

### Build command (exact)
```bash
echo "🚀 Starting Novustell Travel build process..."
pip install --upgrade pip
pip install -r requirements.txt
echo "📦 Dependencies installed successfully"
python manage.py collectstatic --noinput --settings=tours_travels.settings_prod
echo "📁 Static files collected"
python manage.py migrate --settings=tours_travels.settings_prod
echo "🗄️ Database migrations applied"
python manage.py createcachetable --settings=tours_travels.settings_prod
echo "💾 Cache table created"
echo "✅ Build completed successfully"
```

### Start command (exact)
```bash
echo "🌟 Starting Novustell Travel web server..."
gunicorn tours_travels.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers $WEB_CONCURRENCY \
  --timeout $GUNICORN_TIMEOUT \
  --worker-class sync \
  --worker-connections 1000 \
  --max-requests 1000 \
  --max-requests-jitter 100 \
  --preload \
  --access-logfile - \
  --error-logfile - \
  --log-level info
```

### Environment variables set in Render (render.yaml)
(These are injected by Render into the running service. `.env` files are not used on Render.)

Django core
- `DJANGO_SETTINGS_MODULE=tours_travels.settings_prod`
- `PYTHON_VERSION=3.12.0`
- `SECRET_KEY` (generated)
- `DEBUG=False`
- `ALLOWED_HOSTS=novustelltravel.onrender.com,.onrender.com,novustelltravel.com,www.novustelltravel.com`

Database
- `DATABASE_URL` from Render database connection string
- `DB_CONN_MAX_AGE=600`
- `DB_CONN_HEALTH_CHECKS=True`

Server
- `PORT` (generated)
- `WEB_CONCURRENCY=3`
- `GUNICORN_WORKERS=3`
- `GUNICORN_TIMEOUT=120`
- `RENDER_EXTERNAL_HOSTNAME` (generated)

Email (Mailtrap HTTP API)
- `MAILTRAP_API_TOKEN=d766975d57a7ef1acf2f750a36247a37`
- `EMAIL_HOST_USER=api`
- `EMAIL_HOST_PASSWORD=d766975d57a7ef1acf2f750a36247a37`
- `EMAIL_RATE_LIMIT_PER_MINUTE=60`
- `EMAIL_RATE_LIMIT_PER_HOUR=1000`
- `DEFAULT_FROM_EMAIL=Novustell Travel <info@novustelltravel.com>`
- `ADMIN_EMAIL=info@novustelltravel.com`
- `JOBS_EMAIL=careers@novustelltravel.com`
- `NEWSLETTER_EMAIL=news@novustelltravel.com`

Uploadcare
- `UPLOADCARE_PUBLIC_KEY` (sync: false, set manually in Render dashboard)
- `UPLOADCARE_SECRET_KEY` (sync: false, set manually in Render dashboard)

Site configuration
- `SITE_URL=https://wwww.novustelltravel.com`
- `WHATSAPP_PHONE=+254701363551`

Security
- `SECURE_SSL_REDIRECT=True`
- `SECURE_HSTS_SECONDS=31536000`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`
- `SECURE_HSTS_PRELOAD=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `SESSION_COOKIE_HTTPONLY=True`
- `CSRF_COOKIE_HTTPONLY=True`

Performance
- `FILE_UPLOAD_MAX_MEMORY_SIZE=5242880`
- `DATA_UPLOAD_MAX_MEMORY_SIZE=5242880`
- `SESSION_COOKIE_AGE=86400`

Feature flags
- `ENABLE_BOOKING_NOTIFICATIONS=True`
- `ENABLE_EMAIL_MARKETING=True`
- `ENABLE_ANALYTICS=True`
- `ENABLE_CHAT_SUPPORT=False`

Analytics
- `GOOGLE_ANALYTICS_ID=G-JV4GQKWVJL`

Business
- `DEFAULT_BOOKING_EXPIRY_HOURS=24`
- `MAX_BOOKING_ADULTS=20`
- `MAX_BOOKING_CHILDREN=15`
- `MAX_BOOKING_ROOMS=10`

Regional
- `TIME_ZONE=Africa/Nairobi`
- `DEFAULT_LANGUAGE=en`
- `DEFAULT_COUNTRY=Kenya`
- `DEFAULT_CURRENCY=USD`

### Database definition (Render)
- Database name: `novustell-db`
- `databaseName=novustell_travel`
- `user=novustell_user`
- Region: oregon
- Plan: free
- Postgres major version: 15
- `ipAllowList: []` (allows all IPs)

### Celery services in render.yaml
- Celery worker and beat services are present but commented out (deprecated). The current deployment relies on Mailtrap Email Marketing API without background workers.

--------------------------------------------------------------------

## 9) Operational notes for duplication

- Render uses `render.yaml` and dashboard env vars; it does NOT read `.env` files.
- Local development reads `.env` using `python-dotenv` and `python-decouple`.
- `settings_prod.py` expects environment variables to exist for production (particularly `DATABASE_URL` and Mailtrap settings).
- If you duplicate the setup outside Render, ensure the environment variables match `.env.production` or `.env.production.fixed` and that `DJANGO_SETTINGS_MODULE` points to `tours_travels.settings_prod`.
- There is a typo in `render.yaml` for `SITE_URL` (`https://wwww.novustelltravel.com` has four w's). If the target system must match current config exactly, keep it; otherwise correct to `https://www.novustelltravel.com`.

