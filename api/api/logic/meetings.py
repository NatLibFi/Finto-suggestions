import connexion
import inspect  # TODO: remove me


def get_meetings() -> str:
    return inspect.stack()[0][3], 200


def get_meeting(meeting_id: int) -> str:
    return inspect.stack()[0][3], 200


def post_meeting(meeting_id: int) -> str:
    return inspect.stack()[0][3], 200


def delete_meeting(meeting_id: int) -> str:
    return inspect.stack()[0][3], 200


def put_meeting(meeting_id: int) -> str:
    return inspect.stack()[0][3], 200
