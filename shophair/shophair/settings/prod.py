"""
***********************************************************************
************** Author:   Christian KEMGANG NGUESSOP *******************
************** Project:   shophair                  *******************
************** Version:  1.0.0                      *******************
***********************************************************************
"""

# ************PROD************
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("PROD_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#ALLOWED_HOSTS = ["*"]

DBname = os.getenv("PROD_DB_NAME")
DBhost = os.getenv("PROD_DB_HOST")
DBport = os.getenv("PROD_DB_PORT")
DBuser = os.getenv("PROD_DB_USER")
DBpwd = os.getenv("PROD_DB_PASSWORD")

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
