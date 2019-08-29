"""
Authentication related helpers.
See also api.logic.authentication module for auth endpoints.

Token blacklisting partially from
https://github.com/vimalloc/flask-jwt-extended/tree/master/examples/database_blacklist

For additional configuration and features,
please see http://flask-jwt-extended.readthedocs.io/en/latest/
"""

from datetime import datetime
from functools import wraps
from sqlalchemy import exists
from flask_jwt_extended import JWTManager, decode_token, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError

from .models import db, UserRoles, TokenBlacklist


jwt = JWTManager()


class UnauthorizedException(NoAuthorizationError):
    pass


@jwt.token_in_blacklist_loader
def _is_token_revoked(decoded_jwt):
    token = TokenBlacklist.query.filter_by(
        jti=decoded_jwt['jti']).one_or_none()

    return token.revoked if token else False


def set_token_revoked(jwt_id, revoked=True):
    token = TokenBlacklist.query.filter_by(id=jwt_id).one_or_none()
    if token:
        token.revoked = revoked
        db.session.commit()
        return True
    return False


def blacklist_token(jwt, revoked=True):
    decoded_jwt = decode_token(jwt)

    # don't add a new row, if it already exists
    if db.session.query(exists().where(TokenBlacklist.jti == decoded_jwt['jti'])).scalar():
        return False

    token = {
        'jti': decoded_jwt['jti'],
        'token_type': decoded_jwt['type'],
        'expires': datetime.fromtimestamp(decoded_jwt['exp']),
        'revoked': revoked
    }

    db.session.add(TokenBlacklist(**token))
    db.session.commit()

    return True


def prune_expired_tokens():
    """
    Delete all expired tokens from blacklist.
    This should be called once in a while to keep database clean.
    """

    expired = TokenBlacklist.query.filter(
        TokenBlacklist.expires < datetime.now()).all()
    num_deleted = len([db.session.delete(token) for token in expired])
    db.session.commit()

    return num_deleted


def admin_only(f):
    """
    This Flask endpoint decorator ensures that the authorized user
    has a valid (JWT) access token and user role 'ADMIN'.

    Usage:

    @admin_only
    def delete_user(user_id):
        return delete_or_404(User, user_id)
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = get_jwt_identity()

        if not UserRoles[user.get('role')] is UserRoles.ADMIN:
            raise UnauthorizedException(
                "Only an admin is allowed to access this endpoint.")

        return f(*args, **kwargs)
    return wrapper


def authorized(f):
    """
    This Flask endpoint decorator only checks that
    the JWT is still valid (and thus user logged in).
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return f(*args, **kwargs)
    return wrapper


def verify_user_access_to_resource(db_obj):
    """
    Verifies that the user has access to the given resource.
    This happens on three conditions:

    1) User is an admin
    2) User is the owner of the resource
    3) There is no user_id column in the db model (hence no owners)

    @authorized decorator is required in a parent call
    in order for this to work:

    Usage:

    @authorized
    def delete_event(event_id):
        db_obj = model.query.get(primary_key)
        verify_user_access_to_resource(db_obj) # throws an exception
        # delete stuff
    """

    authorized_user = get_jwt_identity()
    if authorized_user and hasattr(db_obj, 'user_id'):
        if UserRoles[authorized_user.get('role')] is UserRoles.ADMIN:
            return
        if not db_obj.user_id == authorized_user.get('id'):
            raise UnauthorizedException(
                'Only owner can access this resource. Please check that user_id matches.')
