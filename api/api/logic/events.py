import connexion
from ..models import Event, Suggestion, db
from ..authentication import authorized
from .common import (get_all_or_404_custom, get_one_or_404, create_or_400, delete_or_404, patch_or_404, update_or_404)
from .validators import event_parameter_validator
from datetime import datetime


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
        return query.order_by(Event.created.asc()).all()

    return get_all_or_404_custom(filter_func)


def get_event(event_id: int) -> str:
    """
    Returns an event by id.

    :param event_id: User id
    :returns: A single event object as json
    """

    return get_one_or_404(Event, event_id)


@authorized
@event_parameter_validator
def post_event() -> str:
    """
    Creates a single event.

    Request body should include a single event object.
    The object should be validated by Connexion according to the API definition.

    :returns: the created event as json
    """

    create_event_response = create_or_400(Event, connexion.request.json)
    if create_event_response is not None and create_event_response[1] is 201:
        try:
            suggestion = Suggestion.query.get(connexion.request.json.get('suggestion_id'))
            if suggestion is not None:
                suggestion.modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                db.session.add(suggestion)
                db.session.commit()
        except ValueError as ex:
            print('Could not update suggestion modified time' + str(ex))

        return create_event_response

@authorized
@event_parameter_validator
def put_event(event_id: int) -> str:
    """
    Updates a single event by id.
    Request body should include a single event object.

    :returns: the created event as json
    """

    return update_or_404(Event, event_id, connexion.request.json)


@authorized
@event_parameter_validator
def patch_event(event_id: int) -> str:
    """
    Patches a single event by id.
    Request body should include a single (partial) event object.

    :returns: the created event as json
    """

    return patch_or_404(Event, event_id, connexion.request.json)


@authorized
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
