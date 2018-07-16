import connexion
import inspect  # TODO: remove me


def get_events() -> str:
    return inspect.stack()[0][3], 200


def get_event(event_id: int) -> str:
    return inspect.stack()[0][3], 200


def post_event(event_id: int) -> str:
    return inspect.stack()[0][3], 200


def delete_event(event_id: int) -> str:
    return inspect.stack()[0][3], 200


def put_event(event_id: int) -> str:
    return inspect.stack()[0][3], 200


def get_events_by_suggestion(suggestion_id: int) -> str:
    return inspect.stack()[0][3], 200


def get_events_by_user(user_id: int) -> str:
    return inspect.stack()[0][3], 200
