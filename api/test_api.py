"""
    `pipenv run pytest` in project root
"""

import pytest
import connexion
from app import app


@pytest.fixture(scope='module')
def client():
    with app.app.test_client() as client:
        yield client


def test_get_suggestions(client):
    response = client.get('api/v1/suggestions')
    assert response.status_code == 200


def test_get_suggestion(client):
    pass


def test_post_suggestion(client):
    pass


def test_put_suggestion(client):
    pass


def test_patch_suggestion(client):
    pass


def test_delete_suggestion(client):
    pass
