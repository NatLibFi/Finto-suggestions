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
    jwt_refresh_token_required,
)

from .common import create_response
from ..models import User
from ..authentication import blacklist_token


def login() -> str:
    """
    Logs the user in returning a valid access token (JWT).

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
            # this time, skip overriden as_dict() to disable event serialization
            serialized_user = super(User, user).as_dict()
            access_token = create_access_token(identity=serialized_user)
            refresh_token = create_refresh_token(identity=serialized_user)

            return create_response({}, 200, access_token=access_token, refresh_token=refresh_token)

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
    Logs the user out by blacklisting the tokens.

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
