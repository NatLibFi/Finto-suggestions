from typing import Dict
import connexion
from ..models import Suggestion, SuggestionTypes, SuggestionStatusTypes
from .common import get_one_or_404, get_all_or_404, create_or_404, delete_or_404, update_or_404


def _suggestion_response_into_model(response: Dict) -> Dict:
    """
    Modifies the response in a way that it fits the Suggestion model schema.
    """

    response['suggestion_type'] = SuggestionTypes(
        response['suggestion_type']).name
    response['status'] = SuggestionStatusTypes(response['status']).name

    return response


def get_suggestions(limit: int = None, offset: int = None) -> str:
    """
    Returns all suggestions.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All suggestion matching the qu in json format
    """

    return get_all_or_404(Suggestion, limit, offset)


def post_suggestion() -> str:
    """
    Creates a single suggestion.

    Request body should include a single suggestion object.
    The object should be validated by Connexion according to the API definition.

    :returns: the created suggestion as json
    """

    suggestion_dict = _suggestion_response_into_model(connexion.request.json)
    return create_or_404(Suggestion, suggestion_dict)


def get_suggestion(suggestion_id: int) -> str:
    """
    Returns a suggestion by id.

    :param id: Suggestion id
    :returns: A single suggestion object as json
    """

    return get_one_or_404(Suggestion, suggestion_id)


def put_suggestion(suggestion_id: int) -> str:
    """
    Updates a single suggestion by id.
    Request body should include a single suggestion object.

    :returns: the created suggestion as json
    """

    suggestion_dict = _suggestion_response_into_model(connexion.request.json)
    return update_or_404(Suggestion, suggestion_id, suggestion_dict)


def delete_suggestion(suggestion_id: int) -> str:
    """
    Deletes a suggestion by id.

    :param id: Suggestion id
    :returns: 204, No Content on success
    """

    return delete_or_404(Suggestion, suggestion_id)
