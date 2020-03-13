from api.logic.common import (create_response, id_exists, get_all_or_400,
                              get_one_or_404, create_or_400, delete_or_404, update_or_404, patch_or_404)
from api.models import User
from .fixtures import USER_DATA, MEETING_DATA, random_user


def _add_single_user(session, user=None):
    if not user:
        user = User(**USER_DATA)
    session.add(user)
    session.commit()

    return user


def test_id_exists(session):
    user = _add_single_user(session)

    assert id_exists(User, user.id)


def test_create_response(session):
    response = create_response(MEETING_DATA, 200, "testing!")

    assert response[0].get('message') == 'testing!'
    assert response[0].get('data').get('name') == MEETING_DATA.get('name')
    assert response[1] == 200


def test_get_all_or_400(session):
    [
        session.add(User(**random_user()))
        for i in range(0, 9)
    ]
    session.commit()

    response = get_all_or_400(User, limit=None, offset=None)
    assert len(response[0].get('data')) == 10

    response = get_all_or_400(User, limit=5, offset=None)
    assert len(response[0].get('data')) == 5

    response = get_all_or_400(User, limit=None, offset=8)
    assert len(response[0].get('data')) == 2


def test_get_one_or_404(session):
    user = _add_single_user(session)

    response = get_one_or_404(User, user.id)
    assert response[1] == 200
    assert response[0].get('data').get('name') == USER_DATA.get('name')

    response = get_one_or_404(User, 999)
    assert response[1] == 404


def test_create_or_400(session):
    response = create_or_400(User, USER_DATA)
    assert response[1] == 201

    # try to create the same user again (same primary keys!)
    response = create_or_400(User, USER_DATA)
    assert response[1] == 400


def test_delete_or_404(session):
    user = _add_single_user(session)

    response = delete_or_404(User, user.id)
    assert response[1] == 204

    # user not found anymore
    response = delete_or_404(User, user.id)
    assert response[1] == 404


def test_update_or_404(session):
    rand_user = random_user()
    user = _add_single_user(session)

    response = update_or_404(User, user.id, rand_user)
    assert response[1] == 200
    assert response[0].get('data').get('name') == rand_user.get('name')

    # user not found on id 999
    response = update_or_404(User, 999, rand_user)
    assert response[1] == 404


def test_patch_or_404(session):
    rand_user = random_user()
    user = _add_single_user(session)

    response = patch_or_404(User, user.id, {'name': 'Mr. Patch'})
    assert response[1] == 200
    assert response[0].get('data').get('name') == 'Mr. Patch'

    # user not found on id 999
    response = patch_or_404(User, 999, rand_user)
    assert response[1] == 404
