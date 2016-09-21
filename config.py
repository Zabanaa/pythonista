class BaseConfig(object):
    DEBUG   = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:msnk2393!.@52.30.100.105/pythonista"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = False

class TestingConfig(BaseConfig):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:msnk2393!.@52.30.100.105/pythonista_tesing"
