import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "your_credentials"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.urandom(24)
    MAIL_SERVER = "Your email server"
    MAIL_PORT = "The default port for the email server (set to 465 if using gmail)"
    MAIL_USE_SSL = True
    MAIL_USERNAME = "your_username"
    MAIL_PASSWORD = "your_password"
    MAIL_DEFAULT_SENDER = "default email address to send from"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "your_credentials"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "your_credentials"

