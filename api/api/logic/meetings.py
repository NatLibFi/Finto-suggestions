import connexion

from ..authentication import admin_only
from ..models import db, Meeting, Suggestion
from .common import (get_one_or_404, get_all_or_400, create_or_400,
                     delete_or_404, update_or_404, patch_or_404,
                     create_response, get_selected_or_400, get_all_or_400_custom)


def get_meetings(limit: int = None, offset: int = None) -> str:
    """
    Returns all meetings.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All meetings matching the query in json format
    """

    return get_all_or_400(Meeting, limit, offset)

def get_meetings_basics(limit: int = None, offset: int = None) -> str:
    """
    Returns id, name, created, modified, meeting_date of meetings.

    Todo: Adjust parameters in the meetings.yaml    

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All meetings matching the query in json format
    """

    return get_selected_or_400(Meeting)


def get_meeting(meeting_id: int) -> str:
    """
    Returns a meeting by id.

    :param meeting_id: Meeting id
    :returns: A single meeting object as json
    """

    return get_one_or_404(Meeting, meeting_id)


@admin_only
def post_meeting() -> str:
    """
    Creates a single meeting.
    Request body should include a single meeting object.

    :returns: the created meeting as json
    """

    return create_or_400(Meeting, connexion.request.json)


@admin_only
def delete_meeting(meeting_id: int) -> str:
    """
    Deletes a meeting by id.

    :param meeting_id: meeting id
    :returns: 204, No Content on success, 404 on error
    """

    return delete_or_404(Meeting, meeting_id)


@admin_only
def put_meeting(meeting_id: int) -> str:
    """
    Updates a single meeting by id.
    Request body should include a single meeting object.

    :returns: the created meeting as json
    """

    return update_or_404(Meeting, meeting_id, connexion.request.json)


@admin_only
def patch_meeting(meeting_id: int) -> str:
    """
    Patches a single meeting by id.
    Request body should include a single (partial) meeting object.

    :returns: the patched meeting as json
    """

    return patch_or_404(Meeting, meeting_id, connexion.request.json)


@admin_only
def add_suggestions_to_meeting(meeting_id: int) -> str:
    """
    Adds the given suggestions to the meeting.

    :returns: the updated meeting as json
    """

    suggestion_ids = connexion.request.json.get('suggestion_ids')
    meeting = Meeting.query.get(meeting_id)

    successfully_added_list = []
    if meeting:
        # update the suggestions one-by-one to overwrite any existing meeting_ids
        # since a suggestion can only be associated with a single meeting at a time
        for suggestion_id in suggestion_ids:
            suggestion = Suggestion.query.get(suggestion_id)
            if suggestion:
                suggestion.meeting_id = meeting_id
                successfully_added_list.append(suggestion_id)

        db.session.commit()

        msg = 'Successfully added {} suggestions (IDs: {}) to meeting {}.'
        return create_response(meeting.as_dict(), 200,
                               msg.format(len(successfully_added_list), successfully_added_list, meeting_id))

    return create_response({}, 404, "Meeting with an id {} doesn't exist.".format(meeting_id))
