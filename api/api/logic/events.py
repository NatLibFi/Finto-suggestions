import connexion
from sqlalchemy.exc import IntegrityError
from ..models import db, Event, Suggestion, User
from .common import create_response, id_exists


def get_events(limit: int = None, offset: int = None, user_id: int = None, suggestion_id: int = None) -> str:
    """
    Returns all events.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All events matching the query in json format
    """

    query = Event.query
    if user_id:
        query = query.filter(Event.user_id == user_id)
    if suggestion_id:
        query = query.filter(Event.suggestion_id == suggestion_id)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    event_objs = query.all()

    if event_objs:
        serialized_objects = [s.as_dict() for s in event_objs]
        return create_response(serialized_objects, 200)
    else:
        return create_response(None, 404, "No events found")


def get_event(event_id: int) -> str:
    """
    Returns an event by id.

    :param event_id: User id
    :returns: A single event object as json
    """

    event_obj = Event.query.get(event_id)
    if event_obj:
        return create_response(event_obj.as_dict(), 200)
    else:
        msg = "Event with an id {} doesn't exist.".format(event_id)
        return create_response(None, 404, msg)


def post_event() -> str:
    """
    Creates a single event.

    Request body should include a single event object.
    The object should be validated by Connexion according to the API definition.

    :returns: the created event as json
    """

    body = connexion.request.json
    event = dict(body)  # copy the response body

    # Check, that the user and/or suggestion exists before continuing the update
    if not id_exists(event.get('user_id'), User):
        return create_response(None, 404, "Given user id {} doesn't exist".format(event.get('user_id')))
    if not id_exists(event.get('suggestion_id'), Suggestion):
        return create_response(None, 404, "Given suggestion id {} doesn't exist".format(event.get('suggestion_id')))

    event_obj = Event(**event)

    try:
        db.session.add(event_obj)
        db.session.commit()
    except IntegrityError:
        msg = "Could not create the event. Perhaps the user_id does not exist?"
        return create_response(None, 404, msg)

    return create_response(event_obj.as_dict(), 200)


def delete_event(event_id: int) -> str:
    """
    Deletes an event by id.

    :param event_id: event id
    :returns: 204, No Content on success
    """

    success = Event.query.filter_by(id=event_id).delete()
    db.session.commit()

    if success:
        return (None, 204)  # No Content
    else:
        msg = "Could not delete event {}. Perhaps it doesn't exist.".format(
            event_id)
        return create_response(None, 404, msg)


def put_event(event_id: int) -> str:
    """
    Updates a single user by id.
    Request body should include a single user object.

    :returns: the created user as json
    """

    # Check, that an existing event is found with the given id
    old_object = Event.query.get(event_id)
    if not old_object:
        msg = "Event with an id {} doesn't exist.".format(event_id)
        return create_response(None, 404, msg)

    body = connexion.request.json
    event = dict(body)  # copy the response body

    # Check, that the user and/or suggestion exists before continuing the update
    if not id_exists(event.get('user_id'), User):
        return create_response(None, 404, "Given user id {} doesn't exist".format(event.get('user_id')))
    if not id_exists(event.get('suggestion_id'), Suggestion):
        return create_response(None, 404, "Given suggestion id {} doesn't exist".format(event.get('suggestion_id')))

    event_obj = Event(**event)
    event_obj.id = old_object.id
    event_obj.created = old_object.created

    try:
        db.session.merge(event_obj)
        db.session.commit()
    except IntegrityError:
        msg = "Could not update the event."
        return create_response(None, 404, msg)

    return create_response(event_obj.as_dict(), 200)


def get_events_by_suggestion(limit: int = None, offset: int = None, suggestion_id: int = None) -> str:
    return get_events(limit=limit, offset=offset, suggestion_id=suggestion_id)


def get_events_by_user(limit: int = None, offset: int = None, user_id: int = None) -> str:
    return get_events(limit=limit, offset=offset, user_id=user_id)
