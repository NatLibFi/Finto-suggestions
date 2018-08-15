import pytest
from api.authentication import authorized, admin_only
from api.models import User, TokenBlacklist
from .conftest import NORMAL_USER


@pytest.fixture(scope='function')
def auhtorized_endpoints(app, session):
    """
    Creates three endpoints, two of which are
    protected by custom authorized access decorators.

    @authorized     any logged in user has access
    @admin_only     only logged in admin user has access
    """

    @app.route('/public', methods=['GET'])
    def protected():
        return "SUCCESS"

    @app.route('/logged_in', methods=['GET'])
    @authorized
    def authorized_test():
        return "SUCCESS"

    @app.route('/admin_only', methods=['GET'])
    @admin_only
    def admin_only_test():
        return "SUCCESS"


def test_access_decorators(client, session, auhtorized_endpoints):
    # All users should have access to /public
    response = client().get('/public')
    assert response.status_code == 200

    response = client('NORMAL').get('/public')
    assert response.status_code == 200

    response = client('ADMIN').get('/public')
    assert response.status_code == 200

    # Only logged in user should have access to /logged_in
    response = client().get('/logged_in')
    assert response.status_code == 401

    response = client('NORMAL').get('/logged_in')
    assert response.status_code == 200

    response = client('ADMIN').get('/logged_in')
    assert response.status_code == 200

    # Only admin user should have access to /admin_only
    response = client().get('/admin_only')
    assert response.status_code == 401

    response = client('NORMAL').get('/admin_only')
    assert response.status_code == 401

    response = client('ADMIN').get('/admin_only')
    assert response.status_code == 200


def _add_user(session, user_obj):
    user = User(**user_obj)
    session.add(user)
    session.commit()

    return user


def _login_user(client, email, password, auth_level=None):
    return client(auth_level).post('/api/login', json={
        'email': email,
        'password': password
    })


def test_login(client, session):
    _add_user(session, NORMAL_USER)

    # Incorret password
    response = _login_user(client, NORMAL_USER['email'], 'wrong password')

    assert response.status_code == 401

    response = _login_user(
        client,
        NORMAL_USER['email'],
        NORMAL_USER['password']
    )

    assert response.status_code == 200
    assert 'access_token' in response.json.keys()
    assert 'refresh_token' in response.json.keys()


def test_logout(client, session):
    _add_user(session, NORMAL_USER)

    login_response = _login_user(
        client,
        NORMAL_USER['email'],
        NORMAL_USER['password']
    )

    response = client('NORMAL').post('/api/logout', json={
        "access_token": login_response.json['access_token'],
        "refresh_token": login_response.json['refresh_token']
    })

    assert response.status_code == 200
    assert len(session.query(TokenBlacklist).all()) == 2


def test_refresh(client, session):
    _add_user(session, NORMAL_USER)

    login_response = _login_user(
        client,
        NORMAL_USER['email'],
        NORMAL_USER['password']
    )

    # set the refresh token as Authorization header
    test_client = client()
    refresh_token = login_response.json.get('refresh_token')
    test_client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {refresh_token}'

    response = test_client.post('/api/refresh')

    assert response.status_code == 200
    assert response.json['access_token'] != login_response.json['access_token']
