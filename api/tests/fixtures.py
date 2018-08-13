import pytest
import sqlalchemy
from sqlalchemy.exc import ProgrammingError, IntegrityError
from app import create_app
from api.models import db, User, UserRoles
from flask_jwt_extended import create_access_token


ADMIN_USER = {
    'name': 'Admin-tester',
    'email': 'admin@test.fi',
    'password': 'password',
    'role': UserRoles.ADMIN
}


NORMAL_USER = {
    'name': 'Normal-tester',
    'email': 'normal@test.fi',
    'password': 'password',
    'role': UserRoles.NORMAL
}


MEETING_DATA = {
    "meeting_date": "2018-08-13T09:59:14.647Z",
    "name": "First Meeting Ever"
}

SUGGESTION_DATA = {
    "alternative_label": {
        "en": "feline animal",
        "fi": "kissaeläin",
        "sv": "katten"
    },
    "broader": [
        "http://www.yso.fi/onto/ysa/Y98177"
    ],
    "description": "Kissaeläimiin kuuluva nelijalkainen nisäkäs.",
    "group": [
        "http://www.yso.fi/onto/ysa/ryhma_07",
        "http://www.yso.fi/onto/ysa/ryhma_09"
    ],
    "meeting_id": 0,
    "narrower": [
        "http://www.yso.fi/onto/ysa/Y98176"
    ],
    "organization": "Ankkalinnan kaupunki",
    "preferred_label": {
        "en": "cat",
        "fi": "kisu",
        "sv": "katten"
    },
    "reason": "Minulla on omat syyni!",
    "related": [
        "http://www.yso.fi/onto/ysa/Y12345"
    ],
    "status": "DEFAULT",
    "suggestion_type": "NEW",
    "tags": [
        "ACCEPTED"
    ],
    "uri": "http://www.yso.fi/onto/ysa/Y505224"
}


@pytest.fixture(scope='session', autouse='true')
def client():
    def client(auth_level=None):
        test_client = flask_app.test_client()

        # add an authorization header for desired role
        if auth_level in access_tokens:
            test_client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(
                access_tokens[auth_level])

        return test_client

    # Create an app with testing configuration
    connexion_app = create_app('config.TestingConfig')
    flask_app = connexion_app.app

    # Initialize the testdb database if it hasn't been created yet
    engine = sqlalchemy.create_engine(
        flask_app.config['SQLALCHEMY_DATABASE_ROOT'] + 'postgres')

    _initialize_test_database(flask_app, engine)
    access_tokens = _initialize_users(flask_app)

    yield client

    _teardown_test_database(flask_app, engine)


def _initialize_test_database(app, engine):
    try:
        with engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            connection.execute("CREATE DATABASE testdb")
    except ProgrammingError:
        pass  # testdb already exists

    with app.app_context():
        db.create_all()


def _teardown_test_database(app, db_engine):
    # teardown
    with app.app_context():
        db.session.remove()
        db.drop_all()

    # with engine.connect() as connection:
    #     connection.execution_options(isolation_level="AUTOCOMMIT")
    #     connection.execute("SET search_path TO psql")
    #     connection.execute("DROP DATABASE testdb")


def _initialize_users(app):
    admin = User(**ADMIN_USER)
    normal = User(**NORMAL_USER)

    with app.app_context():
        try:
            db.session.add(admin)
            db.session.commit()
        except IntegrityError as e:
            db.session().rollback()

        return {
            'ADMIN': create_access_token(
                identity=super(User, admin).as_dict()),
            'NORMAL': create_access_token(
                identity=super(User, normal).as_dict())
        }
