import connexion
from ..models import User
from .common import (get_all_or_404, get_one_or_404,
                     create_or_404, delete_or_404,
                     update_or_404, patch_or_404)


def get_users(limit: int = None, offset: int = None) -> str:
    """
    Returns all users.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All users matching the query in json format
    """

    return get_all_or_404(User, limit, offset)


def get_user(user_id: int) -> str:
    """
    Returns a user by id.

    :param user_id: User id
    :returns: A single user object as json
    """

    return get_one_or_404(User, user_id)


def post_user() -> str:
    """
    Creates a single user.

    Request body should include a single user object.
    The object should be validated by Connexion according to the API definition.

    :returns: the created user as json
    """
    msg = "Unable to create a new user. This email already exists."
    return create_or_404(User, connexion.request.json, error_msg=msg)


def delete_user(user_id: int) -> str:
    """
    Deletes a user by id.

    :param id: user id
    :returns: 204, No Content on success
    """

    return delete_or_404(User, user_id)


def put_user(user_id: int) -> str:
    """
    Updates a single user by id.
    Request body should include a single user object.

    :returns: the created user as json
    """

    return update_or_404(User, user_id, connexion.request.json)


def patch_user(user_id: int) -> str:
    """
    Patches a single user by id.
    Request body should include a single (partial) user object.

    :returns: the patched user as json
    """

    return patch_or_404(User, user_id, connexion.request.json)
