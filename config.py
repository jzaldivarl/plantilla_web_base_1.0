# config.py #

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Wolverine2025'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://flask_user:CodigodeImpacto1983@localhost/flask_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # Configuración de Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
