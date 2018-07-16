import connexion
import inspect  # TODO: remove me


def get_users() -> str:
    return inspect.stack()[0][3], 200


def get_user(user_id: int) -> str:
    return inspect.stack()[0][3], 200


def post_user(user_id: int) -> str:
    return inspect.stack()[0][3], 200


def delete_user(user_id: int) -> str:
    return inspect.stack()[0][3], 200


def put_user(user_id: int) -> str:
    return inspect.stack()[0][3], 200
