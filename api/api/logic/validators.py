"""
  Custom validator decorators for API endpoints.

  The decorator goes through the connexion payload and
  validates/converts the data passing it through to the
  actual api method.

  Swagger handles most of the parameter validation, but
  in some cases, it is necessary to make sure that
  a specific row exists in database before proceeding.

  Usage:

  @suggestions_validator
  def get_suggestion(suggestion_id):
      return get_one_or_404(Suggestion, suggestion_id)
"""

from functools import wraps
import connexion

from .common import create_response, id_exists
from ..models import db, Event, Meeting, Suggestion, Tag, User


def _error_messagify(model):
    msg = "Given {}_id does not exist."
    return msg.format(str(model.__table__)[:-1])


def suggestion_parameter_validator(f):
    @wraps(f)
    def wrapper(*args, **kw):

        payload = connexion.request.json

        # We need to check that meeting_id is a present in request parameters
        # and only after that check that id exists.
        # We check it against None since id 0 is falsy.
        meeting_id = payload.get('meeting_id')
        if meeting_id is not None and not id_exists(Meeting, meeting_id):
            return create_response({}, 404, _error_messagify(Meeting))

        user_id = payload.get('user_id')
        if user_id is not None and not id_exists(User, user_id):
            return create_response({}, 404, _error_messagify(User))

        # tag strings need to be converted to actual tags
        # please note, that nonexisting tags are removed from the list here
        tag_labels = payload.get('tags')
        if tag_labels:
            tag_labels_upper = [label.upper() for label in tag_labels]
            payload['tags'] = db.session.query(
                Tag).filter(Tag.label.in_(tag_labels_upper)).all()

        return f(*args, **kw)

    return wrapper


def suggestion_id_validator(f):
    @wraps(f)
    def wrapper(*args, **kw):

        suggestion_id = kw.get('suggestion_id')
        if suggestion_id is not None and not id_exists(Suggestion, suggestion_id):
            return create_response({}, 404, _error_messagify(Suggestion))

        return f(*args, **kw)

    return wrapper


def reaction_parameter_validator(f):
    @wraps(f)
    def wrapper(*args, **kw):
        payload = connexion.request.json

        # Connexion doesn't support OpenAPI v3.0 yet so no use for oneOf in schema :(
        # https://github.com/zalando/connexion/issues/420
        # Let's do it here

        event_id = payload.get('event_id')
        suggestion_id = payload.get('suggestion_id')

        # Return an error message if both are present or none of either are present
        if (event_id is not None and suggestion_id is not None) or \
           (event_id is None and suggestion_id is None):
            msg = 'Only one of either event_id or suggestion_id is required.'
            return create_response({}, 404, msg)

        if event_id is not None and not id_exists(Event, event_id):
            return create_response({}, 404, _error_messagify(Event))

        if suggestion_id is not None and not id_exists(Suggestion, suggestion_id):
            return create_response({}, 404, _error_messagify(Suggestion))

        user_id = payload.get('user_id')
        if not id_exists(User, user_id):
            return create_response({}, 404, _error_messagify(User))

        return f(*args, **kw)

    return wrapper


def event_parameter_validator(f):
    @wraps(f)
    def wrapper(*args, **kw):
        payload = connexion.request.json

        suggestion_id = payload.get('suggestion_id')
        if suggestion_id is not None and not id_exists(Suggestion, suggestion_id):
            return create_response({}, 404, _error_messagify(Suggestion))

        user_id = payload.get('user_id')
        if user_id is not None and not id_exists(User, user_id):
            return create_response({}, 404, _error_messagify(User))

        # Currently applies also to PATCH!

        # if payload.get('event_type') == 'COMMENT' and user_id is None:
        #     msg = 'A valid user_id is required for events of type `COMMENT`.'
        #     return create_response({}, 404, msg)

        return f(*args, **kw)

    return wrapper
