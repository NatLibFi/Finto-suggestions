import pytest
import sqlalchemy
from sqlalchemy.exc import ProgrammingError, IntegrityError
from flask_jwt_extended import create_access_token
from app import create_app
from api.models import db as _db
from api.models import User, UserRoles


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


@pytest.fixture(scope='session')
def app():
    # Create an app with testing configuration
    connexion_app = create_app('config.TestingConfig')
    flask_app = connexion_app.app

    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    yield flask_app

    ctx.pop()  # teardown


@pytest.fixture(scope='session')
def db(app, request):
    # Initialize the testdb database if it hasn't been created yet
    engine = sqlalchemy.create_engine(
        app.config['SQLALCHEMY_DATABASE_ROOT'] + 'postgres')

    # initialize db
    try:
        with engine.connect() as connection:
            connection.execution_options(isolation_level="AUTOCOMMIT")
            connection.execute("CREATE DATABASE testdb")
    except ProgrammingError:
        pass  # testdb already exists

    _db.app = app
    _db.create_all()

    # yield is not used here,
    # since teardown() is always executed
    # even in case of an exception
    def teardown():
        _db.session.close()
        _db.drop_all()

    request.addfinalizer(teardown)

    return _db


@pytest.fixture(scope='session')
def client(app, db):
    """
    A session-scoped fixture, injecting
    a valid test client with approppriate
    authorization headers to a test case.

    It also initializes the database. This fixture
    is automatically invoked for each test case.

    Usage:

    def test_api_endpoint(client):
        response = client('ADMIN').get('api/endpoint')
        assert response.status_code == 200

    :returns:   a client factory function which takes
                the authorization level as a parameter:
                ('NORMAL', 'ADMIN' or 'None')
    """

    def client(auth_level=None):
        test_client = app.test_client()

        # add an authorization header for desired role
        if auth_level in access_tokens:
            test_client.environ_base['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(
                access_tokens[auth_level])

        return test_client

    access_tokens = _initialize_users(app, db)

    yield client


@pytest.fixture(scope='function')
def session(db):
    """
    Every test function has its own
    scoped session context. Basically all
    database transactions are rolled back
    after the test case is done.
    """

    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


def _initialize_users(app, db):
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
