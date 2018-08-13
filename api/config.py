
class BaseConfig:
    """
    Default values for app configurations. Do not modify these.
    Rather, overwrite the DevelopmentConfig and ProductionConfig values.
    """

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://psql:pw@db:5432/psdb'

    # Disable signals. http://flask-sqlalchemy.pocoo.org/2.1/signals/
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ERROR_MESSAGE_KEY = 'message'
    JWT_BLACKLIST_ENABLED = True

    ENABLE_SWAGGER_UI = False

    DEBUG = False


class DevelopmentConfig(BaseConfig):
    ENABLE_SWAGGER_UI = True
    DEBUG = True


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    # testdb db will be created upon test initialization
    SQLALCHEMY_DATABASE_ROOT = 'postgres://psql:pw@db:5432/'
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_ROOT + 'testdb'
    ENABLE_SWAGGER_UI = False
    DEBUG = True
