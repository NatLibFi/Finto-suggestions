from typing import Dict
import connexion
from ..models import db, Suggestion, SuggestionTypes, SuggestionStatusTypes
from .common import get_one_or_404, get_all_or_404_custom, create_or_404, delete_or_404, update_or_404
from .utils import SUGGESTION_FILTER_FUNCTIONS, SUGGESTION_SORT_FUNCTIONS


def _suggestion_response_into_model(response: Dict) -> Dict:
    """
    Modifies the response in a way that it fits the Suggestion model schema.
    """
    suggestion_type = response.get('suggestion_type')
    status = response.get('status')

    if suggestion_type:
        response['suggestion_type'] = SuggestionTypes(suggestion_type).name
    if status:
        response['status'] = SuggestionStatusTypes(status).name

    return response


def get_suggestions(limit: int = None, offset: int = None, filters: str = None, search: str = None, sort: str = 'DEFAULT') -> str:
    """
    Returns all suggestions.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All suggestion matching the qu in json format
    """

    # TODO: add string search to queries

    def _validate_filters(f):
        # a crude whitelist check for filter types
        return all([f[0].upper() in SUGGESTION_FILTER_FUNCTIONS.keys() for f in filters])

    def query_func():
        if sort in SUGGESTION_SORT_FUNCTIONS:
            query = SUGGESTION_SORT_FUNCTIONS.get(sort)(db.session)

        if filters and _validate_filters(filters):
            for name, value in filters:
                filter_func = SUGGESTION_FILTER_FUNCTIONS.get(name.upper())
                if filter_func:
                    query = filter_func(query, value.upper())

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        return query.all()

    if filters:
        # status:accepted|type:new|meeting:12
        # -> [['status', 'accepted'], ['type', 'new'], ['meeting', '12']]
        filters = [f.split(':') for f in filters.split('|')]

    return get_all_or_404_custom(query_func)


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
