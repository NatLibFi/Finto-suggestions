import connexion
import inspect  # TODO: remove me


def get_tags() -> str:
    return inspect.stack()[0][3], 200


def get_tag(tag_id: int) -> str:
    return inspect.stack()[0][3], 200


def post_tag(tag_id: int) -> str:
    return inspect.stack()[0][3], 200


def delete_tag(tag_id: int) -> str:
    return inspect.stack()[0][3], 200


def put_tag(tag_id: int) -> str:
    return inspect.stack()[0][3], 200
