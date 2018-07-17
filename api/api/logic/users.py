import connexion
from ..models import db, User
from .common import create_response
from sqlalchemy.exc import IntegrityError


def get_users(limit: int = None, offset: int = None) -> str:
    """
    Returns all users.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All users matching the query in json format
    """

    query = User.query
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    user_objs = query.all()

    if user_objs:
        serialized_objects = [s.as_dict() for s in user_objs]
        return create_response(serialized_objects, 200)
    else:
        return create_response(None, 404, "No users found")


def get_user(user_id: int) -> str:
    """
    Returns a user by id.

    :param user_id: User id
    :returns: A single user object as json
    """

    user_obj = User.query.get(user_id)
    if user_obj:
        return create_response(user_obj.as_dict(), 200)
    else:
        msg = "User with an id {} doesn't exist.".format(user_id)
        return create_response(None, 404, msg)


def post_user() -> str:
    """
    Creates a single user.

    Request body should include a single user object.
    The object should be validated by Connexion according to the API definition.

    :returns: the created user as json
    """

    body = connexion.request.json
    user = dict(body)  # copy the response body

    password = user.pop('password')
    user_obj = User(**user)
    user_obj.hash_password(password)

    try:
        db.session.add(user_obj)
        db.session.commit()
    except IntegrityError:
        msg = "A user with the same name or email already exists."
        return create_response(None, 404, msg)

    return create_response(user_obj.as_dict(), 200)


def delete_user(user_id: int) -> str:
    """
    Deletes a user by id.

    :param id: user id
    :returns: 204, No Content on success
    """

    success = User.query.filter_by(id=user_id).delete()
    db.session.commit()

    if success:
        return (None, 204)  # No Content
    else:
        msg = "Could not delete user {}. Perhaps it doesn't exist.".format(
            user_id)
        return create_response(None, 404, msg)


def put_user(user_id: int) -> str:
    """
    Updates a single user by id.
    Request body should include a single user object.

    :returns: the created user as json
    """

    # TODO: this should be a protected endpoint
    # and only ADMIN users OR owner can update it

    old_object = User.query.get(user_id)
    if not old_object:
        msg = "User with an id {} doesn't exist.".format(user_id)
        return create_response(None, 404, msg)

    body = connexion.request.json
    user = dict(body)  # copy the response body

    password = user.pop('password')
    user_obj = User(**user)
    user_obj.hash_password(password)

    user_obj.id = old_object.id
    user_obj.created = old_object.created

    db.session.merge(user_obj)
    db.session.commit()

    return create_response(user_obj.as_dict(), 200)
