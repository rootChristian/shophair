"""
***********************************************************************
************** Author:   Christian KEMGANG NGUESSOP *******************
************** Project:   shophair                  *******************
************** Version:  1.0.0                      *******************
***********************************************************************
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Permet que toutes nos URLs se terminent par une barre oblique
APPEND_SLASH = True

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # External packages
    'corsheaders',
    "rest_framework",
    "rest_framework_simplejwt",
    #'rest_framework_simplejwt.token_blacklist',
    # Internal Apps
    "accounts"
    #"users",
    #"locations",
    #"categories",
    #"products",
    #"orders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# To use my own model user
AUTH_USER_MODEL = 'accounts.User'

ROOT_URLCONF = "shophair.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "shophair.wsgi.application"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Authentification
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# Set time token
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '88d9-2a01-e0a-198-3970-7d08-b96b-1d13-57e6.ngrok-free.app',  # Remplace par ton domaine ngrok
]
'''
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://example.com",
]
'''

# Configuration variable to sending an email
EMAIL_HOST=os.getenv("EMAIL_HOST")
EMAIL_HOST_USER=os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD=os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL=os.getenv("DEFAULT_FROM_EMAIL")
EMAIL_USE_TLS=os.getenv("EMAIL_USE_TLS")
EMAIL_PORT=os.getenv("EMAIL_PORT")

# Google client OAuth configuration
GOOGLE_CLIENT_ID=os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET=os.getenv("GOOGLE_CLIENT_SECRET")
SOCIAL_AUTH_PASSWORD=os.getenv("DEFAULT_AUTH_PASSWORD")
