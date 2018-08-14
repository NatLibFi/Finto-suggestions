# from .fixtures import *
from .fixtures import MEETING_DATA
from api.models import Meeting


def _add_meetings(session, n):
    meetings = [Meeting(**MEETING_DATA) for i in range(0, n)]
    for m in meetings:
        session.add(m)
    session.commit()
    return [m.id for m in meetings]


def test_post_meeting(client, session):
    # Unauthorized
    response = client().post('api/meetings/', json=MEETING_DATA)
    assert response.status_code == 401

    # Normal
    response = client('NORMAL').post('api/meetings/', json=MEETING_DATA)
    assert response.status_code == 401

    # Admin
    response = client('ADMIN').post('api/meetings/', json=MEETING_DATA)
    assert response.status_code == 201


def test_get_meetings(client, session):
    _add_meetings(session, 3)

    response = client().get('api/meetings/')

    assert response.status_code == 200
    assert isinstance(response.json.get('data'), list)
    assert len(response.json.get('data')) == 3


def test_get_meeting(client, session):
    meeting_id = _add_meetings(session, 1)[0]
    response = client().get(f'api/meetings/{meeting_id}')

    assert response.status_code == 200
