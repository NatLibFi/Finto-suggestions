import connexion
from sqlalchemy.exc import IntegrityError
from ..models import db, Meeting
from .common import create_response, id_exists, get_one_or_404, get_all_or_404, create_or_404, delete_or_404, update_or_404

import inspect  # TODO: remove me


def get_meetings(limit: int = None, offset: int = None) -> str:
    """
    Returns all meetings.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All meetings matching the query in json format
    """

    return get_all_or_404(Meeting, limit, offset)


def get_meeting(meeting_id: int) -> str:
    """
    Returns a meeting by id.

    :param meeting_id: Meeting id
    :returns: A single meeting object as json
    """

    return get_one_or_404(Meeting, meeting_id)


def post_meeting() -> str:
    """
    Creates a single meeting.
    Request body should include a single meeting object.

    :returns: the created meeting as json
    """

    return create_or_404(Meeting, connexion.request.json)


def delete_meeting(meeting_id: int) -> str:
    """
    Deletes a meeting by id.

    :param meeting_id: meeting id
    :returns: 204, No Content on success, 404 on error
    """

    return delete_or_404(Meeting, meeting_id)


def put_meeting(meeting_id: int) -> str:
    """
    Updates a single meeting by id.
    Request body should include a single meeting object.

    :returns: the created meeting as json
    """

    return update_or_404(Meeting, meeting_id, connexion.request.json)
