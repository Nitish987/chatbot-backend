import firebase_admin
from pathlib import Path
from dotenv import load_dotenv
from os import getenv
from firebase_admin import credentials
from corsheaders.defaults import default_headers

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

APP_NAME = getenv('APP_NAME')

SECRET_KEY = getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = [getenv('HOST_IP')]


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
    'app.index',
    'app.account',
    'app.project',
    'app.apis',
    'app.chatbot',
    'app.emforms',
    'app.external',
    'app.billing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'

# User Model

AUTH_USER_MODEL = 'account.User'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': getenv('DATABASE_NAME'),
#         'USER': getenv('DATABASE_USER'),
#         'PASSWORD': getenv('DATABASE_PASSWORD'),
#         'HOST': getenv('DATABASE_HOST'),
#         'PORT': getenv('DATABASE_PORT'),
#         'OPTIONS': {
#             'charset': 'utf8mb4',
#         },
#     }
# }

# Firebase
creds = credentials.Certificate(str(BASE_DIR / 'firebase_credentials.json'))
firebase_admin.initialize_app(creds)

# Password validation

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

# Rest API Framework Configurations

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'common.auth.authentication.UserAuthentication',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'signup': '10/min',
        'signup_verification': '100/min',
        'resent_signup_otp': '10/min',
        'login': '10/min',
        'password_recovery': '10/min',
        'password_recovery_verification': '100/min',
        'password_recovery_new_password': '10/min',
        'resent_password_recovery_otp': '10/min',
        'authenticated_user': '1000/hour',
        'change_names': '3/day',
        'logout': '10/min',
    },
    'EXCEPTION_HANDLER': 'common.exception.exception_handler.ExceptionHandler'
}

# Jwt Config

JWT_ACCESS_SECRET = getenv('JWT_ACCESS_SECRET')
JWT_REFRESH_SECRET = getenv('JWT_REFRESH_SECRET')

# App api key

APP_API_KEY = getenv('APP_API_KEY')

# Account Creation Key

ACCOUNT_CREATION_KEY = getenv('ACCOUNT_CREATION_KEY')

# Encryption Key

SERVER_ENC_KEY = getenv('SERVER_ENC_KEY')

# External api key

EXTERNAL_SERVER_API_KEY = getenv('EXTERNAL_SERVER_API_KEY')

# Cors Configuration

CORS_ALLOWED_ORIGINS = [getenv('CLIENT_ORIGIN')]
CORS_ALLOW_HEADERS = (*default_headers, 'UID')
CORS_ALLOW_CREDENTIALS = True

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATICFILES_DIRS  = [BASE_DIR / 'static']

# Media files (Uploaded files)

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
