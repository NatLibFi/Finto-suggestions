from .fixtures import *


def test_post_meeting(client):
    # Unauthorized
    response = client().post('api/meetings/', json=MEETING_DATA)
    assert response.status_code == 401

    # Normal
    response = client('NORMAL').post('api/meetings/', json=MEETING_DATA)
    assert response.status_code == 401

    # Admin
    response = client('ADMIN').post('api/meetings/', json=MEETING_DATA)
    assert response.status_code == 201


def test_get_meetings(client):
    response = client().get('api/meetings/')
    assert response.status_code == 200
    assert isinstance(response.json.get('data'), list)
    assert len(response.json.get('data')) == 1


def test_get_meeting(client):
    response = client().get('api/meetings/1')
    assert response.status_code == 200
