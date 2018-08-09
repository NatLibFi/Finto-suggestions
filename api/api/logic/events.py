import connexion
from ..models import Event, Suggestion, User
from .common import (create_response, id_exists, get_all_or_404_custom,
                     get_one_or_404, create_or_404, delete_or_404,
                     patch_or_404, update_or_404)
from .validators import events_validator


def get_events(limit: int = None, offset: int = None, user_id: int = None, suggestion_id: int = None) -> str:
    """
    Returns all events.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All events matching the query in json format
    """

    def filter_func():
        query = Event.query
        if user_id:
            query = query.filter(Event.user_id == user_id)
        if suggestion_id:
            query = query.filter(Event.suggestion_id == suggestion_id)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        return query.all()

    return get_all_or_404_custom(filter_func)


def get_event(event_id: int) -> str:
    """
    Returns an event by id.

    :param event_id: User id
    :returns: A single event object as json
    """

    return get_one_or_404(Event, event_id)


@events_validator
def post_event() -> str:
    """
    Creates a single event.

    Request body should include a single event object.
    The object should be validated by Connexion according to the API definition.

    :returns: the created event as json
    """

    return create_or_404(Event, connexion.request.json)


@events_validator
def put_event(event_id: int) -> str:
    """
    Updates a single event by id.
    Request body should include a single event object.

    :returns: the created event as json
    """

    return update_or_404(Event, event_id, connexion.request.json)


@events_validator
def patch_event(event_id: int) -> str:
    """
    Patcjes a single event by id.
    Request body should include a single (partial) event object.

    :returns: the created event as json
    """

    return patch_or_404(Event, event_id, connexion.request.json)


def delete_event(event_id: int) -> str:
    """
    Deletes an event by id.

    :param event_id: event id
    :returns: 204, No Content on success
    """

    return delete_or_404(Event, event_id)


def get_events_by_suggestion(limit: int = None, offset: int = None, suggestion_id: int = None) -> str:
    return get_events(limit=limit, offset=offset, suggestion_id=suggestion_id)


def get_events_by_user(limit: int = None, offset: int = None, user_id: int = None) -> str:
    return get_events(limit=limit, offset=offset, user_id=user_id)
