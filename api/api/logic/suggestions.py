import connexion
from ..models import db, Suggestion, SuggestionTypes, SuggestionStatusTypes
from datetime import datetime
from typing import Dict, List, Union
from .common import create_response


def _suggestion_response_into_model(response: Dict) -> Dict:
    """
    Modifies the response in a way that it fits the Suggestion model schema.
    """

    response['suggestion_type'] = SuggestionTypes(
        response['suggestion_type']).name
    response['status'] = SuggestionStatusTypes(response['status']).name
    response['modified'] = datetime.utcnow()

    return response


def get_suggestions(limit: int = None, offset: int = None) -> str:
    """
    Returns all suggestions.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offest: Start the query from offset (e.g. for paging)
    :returns: All suggestion matching the qu in json format
    """

    query = Suggestion.query
    if (limit):
        query = query.limit(limit)
    if (offset):
        query = query.offset(offset)
    suggestion_objs = query.all()

    if suggestion_objs:
        serialized_objects = [s.as_dict() for s in suggestion_objs]
        return create_response(serialized_objects, 200)
    else:
        return create_response(None, 404, "No suggestions found")


def post_suggestion() -> str:
    """
    Creates a single suggestion.

    Request body should include a single suggestion object.
    The object should be validated by Connexion according to the API definition.

    :returns: the created suggestion as json
    """

    body = connexion.request.json
    suggestion = dict(body)  # copy the response body
    suggestion = _suggestion_response_into_model(suggestion)
    # TODO: is the status parameter necessary here?

    suggestion_obj = Suggestion(**suggestion)
    db.session.add(suggestion_obj)
    db.session.commit()

    return {
        "data": suggestion_obj.as_dict()
    }


def get_suggestion(suggestion_id: int) -> str:
    """
    Returns a suggestion by id.

    :param id: Suggestion id
    :returns: A single suggestion object as json
    """

    suggestion_obj = Suggestion.query.get(suggestion_id)
    if suggestion_obj:
        return create_response(suggestion_obj.as_dict(), 200)
    else:
        msg = "Suggestion with an id {} doesn't exist.".format(suggestion_id)
        return create_response(None, 404, msg)


def put_suggestion(suggestion_id: int) -> str:
    """
    Updates a single suggestion by id.
    Request body should include a single suggestion object.

    :returns: the created suggestion as json
    """

    old_object = Suggestion.query.get(suggestion_id)
    if not old_object:
        msg = "Suggestion with an id {} doesn't exist.".format(suggestion_id)
        return create_response(None, 404, msg)

    body = connexion.request.json
    suggestion = dict(body)  # copy the response body
    suggestion = _suggestion_response_into_model(suggestion)

    # create a new suggestion, but replace its id
    suggestion_obj = Suggestion(**suggestion)
    suggestion_obj.id = old_object.id
    suggestion_obj.created = old_object.created

    db.session.merge(suggestion_obj)
    db.session.commit()

    return create_response(suggestion_obj.as_dict(), 200)


def delete_suggestion(suggestion_id: int) -> str:
    """
    Deletes a suggestion by id.

    :param id: Suggestion id
    :returns: 204 No Content on success
    """

    success = Suggestion.query.filter_by(id=suggestion_id).delete()
    db.session.commit()

    if success:
        return (None, 204)  # No Content
    else:
        msg = "Could not delete suggestion {}. Perhaps it doesn't exist.".format(
            suggestion_id)
        return create_response(None, 404, msg)
