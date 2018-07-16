import connexion
import inspect  # TODO: remove me


def get_reactions() -> str:
    return inspect.stack()[0][3], 200


def get_reaction(reaction_id: int) -> str:
    return inspect.stack()[0][3], 200


def post_reaction(reaction_id: int) -> str:
    return inspect.stack()[0][3], 200


def delete_reaction(reaction_id: int) -> str:
    return inspect.stack()[0][3], 200


def put_reaction(reaction_id: int) -> str:
    return inspect.stack()[0][3], 200
