"""
Flask configuration:

    Generating a SECRET_KEY with python:
        import binascii
        import os

        binascii.hexlify(os.urandom(24))

    Setting up GMAIL mail server:
        Insure less secure apps in enabled in settings
        Generate a app password for your app in gmail security settings

    Sensitive config data will be imported from /etc/flask_config.json:
        {
            "SECRET_KEY": "Your secret key here",
            "MAIL_USERNAME": "Your_email@gmail.com",
            "MAIL_PASSWORD": "Your app password here"
        }




"""
from datetime import timedelta
import json

with open('/etc/flask_config.json') as config_file:
    config = json.load(config_file)


class Config:
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SECRET_KEY = config.get('SECRET_KEY')
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=3)
    SESSION_COOKIE_SAMESITE = 'Lax'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = config.get('MAIL_USERNAME')
    MAIL_PASSWORD = config.get('MAIL_PASSWORD')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
