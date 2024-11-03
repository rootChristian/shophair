"""
***********************************************************************
************** Author:   Christian KEMGANG NGUESSOP *******************
************** Project:   shophair                  *******************
************** Version:  1.0.0                      *******************
***********************************************************************
"""

# ************DEV************
from .base import *

DBname = os.getenv("DEV_DB_NAME")
DBhost = os.getenv("DEV_DB_HOST")
DBport = os.getenv("DEV_DB_PORT")
DBuser = os.getenv("DEV_DB_USER")
DBpwd = os.getenv("DEV_DB_PASSWORD")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DEV_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DBname,
        'USER': DBuser,
        'PASSWORD': DBpwd,
        'HOST': DBhost,
        'PORT': DBport
    }
}
    