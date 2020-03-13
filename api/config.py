import os

user = os.environ.get('POSTGRES_USER')
pw = os.environ.get('POSTGRES_PASSWORD')
db = os.environ.get('POSTGRES_DB')

class BaseConfig:
    """
    Default values for app configurations. Do not modify these.
    Rather, overwrite the DevelopmentConfig and ProductionConfig values.
    """
    # SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{pw}@db:5432/{db}'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{pw}@db:5432/{db}?client_encoding=utf8'

    # Disable signals. http://flask-sqlalchemy.pocoo.org/2.1/signals/
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True

    # Was not enabled on thu 26.9.19 ENABLE_SWAGGER_UI = False
    ENABLE_SWAGGER_UI = True

    DEBUG = False

class DevelopmentConfig(BaseConfig):
    # db_container_name = 'db'
    # ENABLE_SWAGGER_UI = True
    DEBUG = True

class TestingConfig(BaseConfig):
    # testdb db will be created upon test initialization
    # ENABLE_SWAGGER_UI = True
    SQLALCHEMY_DATABASE_ROOT = f'postgresql+psycopg2://{user}:{pw}@db:5432/'
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_ROOT + 'testdb'
    #db_container_name = 'db'
    #SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{pw}@{db_container_name}:5432/{db}'
    DEBUG = True

class ProductionConfig(BaseConfig):
    # ENABLE_SWAGGER_UI = True
    db_container_name = 'db'
    SQLALCHEMY_DATABASE_URI = f'postgresql://{user}:{pw}@{db_container_name}:5432/{db}'
    DEBUG = False
