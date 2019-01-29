import connexion
from ..authentication import admin_only
from ..models import User, db
from .common import (get_all_or_404, get_one_or_404, create_or_404, delete_or_404, update_or_404, patch_or_404)

import string
import random
import smtplib, ssl, os


@admin_only
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


@admin_only
def delete_user(user_id: int) -> str:
    """
    Deletes a user by id.

    :param id: user id
    :returns: 204, No Content on success
    """

    return delete_or_404(User, user_id)


@admin_only
def put_user(user_id: int) -> str:
    """
    Updates a single user by id.
    Request body should include a single user object.

    :returns: the created user as json
    """

    return update_or_404(User, user_id, connexion.request.json)


@admin_only
def patch_user(user_id: int) -> str:
    """
    Patches a single user by id.
    Request body should include a single (partial) user object.

    :returns: the patched user as json
    """

    return patch_or_404(User, user_id, connexion.request.json)


def put_reset_password() -> str:
    """
    Reset password by email
    :returns 202 if success, other return 401
    """

    email = connexion.request.json.get('email')
    print(email)

    if email is not None and len(email) > 0:
      user = User.query.filter_by(email=email).first()

      if user is not None:
        password_length = 8
        new_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=password_length))
        user.password = new_password

        password_update_success = False

        try:
          db.session.add(user);
          db.session.commit()
          password_update_success = True
        except ValueError as ex:
          print(str(ex))
          db.session.rollback()
          return { 'error': str(ex), 'code': 400 }, 400

        if password_update_success is True:
          print('password updated to user')
          send_email(new_password, user.email)

    return { 'code': 200 }, 200


def send_email(password: str, email: str) -> str:
    """
    Method for sending email messages
    """

    server = smtplib.SMTP('localhost', 1025)

    #Next, log in to the server
    # server.login("youremailusername", "password")

    #Send the mail
    msg = """\
    Hello!" # The /n separates the message from the headers
    """
    server.sendmail("noreply@localhost", email, msg)
    server.quit()

    return