import os

user = os.environ.get('POSTGRES_USER')
pw = os.environ.get('POSTGRES_PASSWORD')
db = os.environ.get('POSTGRES_DB')


class BaseConfig:
    """
    Default values for app configurations. Do not modify these.
    Rather, overwrite the DevelopmentConfig and ProductionConfig values.
    """
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{pw}@db:5432/{db}'

    # Disable signals. http://flask-sqlalchemy.pocoo.org/2.1/signals/
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True

    CORS_ALLOWED_ORIGINS = ['finto.fi']

    ENABLE_SWAGGER_UI = False

    DEBUG = False


class DevelopmentConfig(BaseConfig):
    ENABLE_SWAGGER_UI = True
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    # testdb db will be created upon test initialization
    SQLALCHEMY_DATABASE_ROOT = f'postgresql+psycopg2://{user}:{pw}@db:5432/'
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_ROOT + 'testdb'
    ENABLE_SWAGGER_UI = False
    DEBUG = True
