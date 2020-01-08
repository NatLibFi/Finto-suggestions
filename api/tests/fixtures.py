import uuid
import copy

from api.models import UserRoles


MEETING_DATA = {
    "meeting_date": "2018-08-13T09:59:14.647Z",
    "name": "First Meeting Ever"
}


USER_DATA = {
    'name': 'Normal-tester',
    'email': 'normal@test.fi',
    'password': 'password',
    'role': UserRoles.NORMAL
}


def random_user():
    return _randomize_dict(USER_DATA, ['name', 'email', 'password'])


def _randomize_dict(model_data, fields):
    """
    Randomizes the string and integer keys in a dumb, but working way.
    """
    data_object = copy.deepcopy(model_data)
    n = 0

    for key in data_object.keys():
        if key in fields:
            if isinstance(key, str):
                data_object[key] = uuid.uuid4().hex[:6]
            elif isinstance(key, int):
                data_object[key] = n
                n += 1

    return data_object
