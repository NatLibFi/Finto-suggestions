from typing import Dict, List, Union

from sqlalchemy import exists
from ..models import db


def create_response(data: Dict, status_code: int, message: str = None) -> Dict:
    response_dict = {}
    response_dict["data"] = data
    if message:
        response_dict["message"] = message
    response_dict["code"] = status_code

    return response_dict, status_code


def id_exists(id: int, model: object) -> bool:
    """
    Checks if the given id exists in the given model object.

    :param id: id to search
    :param model: model to search from
    :returns: True if id exists, or id is None. False if user was not found in the model.
    """

    if id and not db.session.query(exists().where(model.id == id)).scalar():
        return False
    return True
