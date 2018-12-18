"""
Authentication related API Endpoints.

Authentication flow:
    1.) A registered user acquires an accesst token (JSON Web Token, JWT) by logging in.
        (This can be tested from the Swagger UI, for example: /api/ui -> /login)
        Also refresh token is acquired.
    2.) Now authenticated user can access auth-only API endpoints by adding a
            Authorization: Bearer <access token>
        header to requests.
    3.) The access token has a default expiration of 15 minutes. The user needs to get
        a new token from the /api/refresh endpoint using the refresh token. It has a
        default expiration of 30 days.


Decorator @jwt_required (from flask_jwt_extended) should be added for each
API operation that requires authenticated access.

Token blacklisting partially from
https://github.com/vimalloc/flask-jwt-extended/tree/master/examples/database_blacklist

For additional configuration and features,
please see http://flask-jwt-extended.readthedocs.io/en/latest/
"""


import connexion

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    jwt_refresh_token_required
)

from .common import create_response
from ..models import db, User, UserRoles, AccessToken
from ..authentication import blacklist_token

import requests
import os


def login() -> str:
    """
    Logs the user in returning a valid access token (JWT) and user_id.

    POST request requires a body with user email and password.
    This should be sent over https!

    {
        "email": "test@test.com",
        "password": "mysecretpassword"
    }

    :returns: A JWT access token wrapped in a response object or an error message
    """

    email = connexion.request.json.get('email', None)
    password = connexion.request.json.get('password', None)

    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and user.validate_password(password):
            # this time, skip overriden as_dict() to disable event
            # serialization
            serialized_user = super(User, user).as_dict()
            access_token = create_access_token(identity=serialized_user)
            refresh_token = create_refresh_token(identity=serialized_user)

            return {'access_token': access_token, 'refresh_token': refresh_token, 'user_id': user.id, 'code': 200}, 200

    return create_response(None, 401, "Incorrect email or password.")


@jwt_refresh_token_required
def refresh() -> str:
    """
    Refreshes the JWT access token with a refresh token.

    Requires the following header to get a fresh access token
        Authorization: Bearer <valid refresh token>

    :returns: A JWT access token wrapped in a response object
    """

    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    return create_response({}, 200, access_token=access_token)


@jwt_required
def logout() -> str:
    """
    Log the user out by blacklisting the tokens.

    POST request requires a body with
    an access_token and refresh_token.

    {
        "access_token": "eyJ0eXAiOiJKV1Q...",
        "refresh_token": "eyJ0eXAiOiJKV1..."
    }

    :returns: A JWT access token wrapped in a response object or an error message
    """

    access_token = connexion.request.json.get('access_token', None)
    refresh_token = connexion.request.json.get('refresh_token', None)

    if access_token and refresh_token:
        blacklist_token(access_token)
        blacklist_token(refresh_token)

    return create_response({}, 200, "Successfully logged out.")


@jwt_required
def revokeAuthentication() -> str:
    """
    Log the user out by blacklisting the tokens.

    POST request requires a body with
    an access_token and refresh_token.

    {
        "access_token": "eyJ0eXAiOiJKV1Q...",
        "refresh_token": "eyJ0eXAiOiJKV1..."
    }

    :returns: A JWT access token wrapped in a response object or an error message
    """

    user_id = connexion.request.json.get('user_id', None)

    try:
        if user_id is not None and user_id > 0:
            tokens = AccessToken.query.filter_by(user_id=user_id).all()
            if tokens is not None and len(tokens) > 0:
                for token in tokens:
                    if token.provider is 'local':
                        blacklist_token(token.access_token)
                        blacklist_token(token.refresh_token)
                    AccessToken.query.filter_by(id=token.id).delete()

            return create_response({}, 200, 'Successfully revoked user authentication tokens.')

    except Exception as ex:
        print(ex)
        db.session.rollback()

    return create_response({}, 200, 'There was errors while trying to blacklist and remove tokens ')


def post_github() -> str:
    """
    Callback method for Github oAuth2 authorization

    :returns: A JWT access token wrapped in a response object or an error message
    """

    code = connexion.request.json.get('code')
    state = connexion.request.json.get('state')

    oauth_data = ()
    try:
      oauth_data = handle_github_request(code, state)
      return handle_user_creation(code, oauth_data)
    except ValueError as ex:
      print(ex)
      return { 'error': str(ex) }, 400


def handle_github_request(code, state) -> (str, str):
    """
    Handles github request
    :returns tuple(name, email, provider=github, github_access_token) or valueerror exception

    """

    name = ''
    email = ''
    provider_name = 'github'
    github_access_token = ''

    if code is not None and state is not None:
        if state is '0':

            github_client_id = os.environ.get('GITHUB_CLIENT_ID')
            github_client_secret = os.environ.get('GITHUB_CLIENT_SECRET')
            redirect_uri = os.environ.get('GITHUB_REDIRECT_URI')

            payload = {
              'client_id': github_client_id,
              'client_secret': github_client_secret,
              'code': code,
              'redirect_uri': redirect_uri
              }

            token_response = requests.post(
                'https://github.com/login/oauth/access_token', data=payload)

            if len(token_response.text) > 0:
                github_access_token = token_response.text.split('&')[
                                                                0].split('=')[1]

            if github_access_token is not None and len(github_access_token) > 0:

              user_data_response = requests.get(
                  'https://api.github.com/user?access_token=' + github_access_token)

              if user_data_response.ok is True:
                user_data = user_data_response.json()
                print(user_data)
                name = user_data['name']

                user_email_data_response = requests.get(
                    'https://api.github.com/user/emails?access_token=' + github_access_token)

                if user_email_data_response.ok is True:
                    user_email_data = user_email_data_response.json()
                    print(user_email_data)
                    for data in user_email_data:
                        if data['primary'] is True:
                            email = data['email']

    if name is not None and email is not None:
        return (name, email, provider_name, github_access_token)
    else:
        raise ValueError('name and email values are not valid')


def handle_user_creation(code, oauth_data) -> str:
    """
    Handles user creation
    :parameters oauth application code and oauthdata(name, email, provider, oauht_access_token)
    :returns success response or exception that is upper method catched
    """

    name = oauth_data[0]
    email = oauth_data[1]
    provider = oauth_data[2]
    oauth_access_token = oauth_data[3]
    local_access_token = ''

    user = User.query.filter_by(email=email).first()

    if user is None:
        user = User(
          name=name,
          email=email,
          password=None,
          role=UserRoles.NORMAL
        )

        try:
            db.session.add(user)
            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            raise ex

        existing_ext_token = AccessToken.query.filter_by(user_id=user.id).first()

        if existing_ext_token is not None:
            db.session.delete(existing_ext_token)

        ext_token = AccessToken(user_id=user.id, provider=provider, code=code, access_token=oauth_access_token)

        try:
            db.session.add(ext_token)
            db.session.commit()

        except Exception as ex:
            db.session.rollback()
            raise ex

        serialized_user = super(User, user).as_dict()
        local_access_token = create_access_token(identity=serialized_user)
        refresh_token = create_refresh_token(identity=serialized_user)

        token = AccessToken(user_id=user.id, provider='local', access_token=local_access_token, refresh_token=refresh_token)

        try:
          db.session.add(token)
          db.session.commit()
        except Exception as ex:
          db.session.rollback()
          raise ex

    return {'access_token' : local_access_token, 'user_id': user.id}, 200

def get_github() -> str:
  return 200
