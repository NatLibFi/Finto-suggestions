from datetime import datetime
from sqlalchemy import exists
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import JWTManager, decode_token

from .models import db, User, TokenBlacklist


jwt = JWTManager()


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
