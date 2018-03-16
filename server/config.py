import secrets

from flask import current_app

DEBUG = True
SECRET_KEY = secrets.SECRET_KEY

MONGODB_DB = 'mydatabase'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

REDIS_HOST = ''

# CORS Config

# Email Config
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = secrets.MAIL_USERNAME
MAIL_PASSWORD = secrets.MAIL_PASSWORD
MAIL_USE_TLS = False
MAIL_USE_SSL = True
