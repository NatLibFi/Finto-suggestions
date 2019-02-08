import connexion
from sqlalchemy import or_
from sqlalchemy.types import Unicode
from ..authentication import admin_only
from .validators import suggestion_parameter_validator, suggestion_id_validator, _error_messagify
from .common import (create_response, get_one_or_404, get_all_or_404_custom,
                     create_or_404, delete_or_404, patch_or_404, update_or_404)
from .utils import SUGGESTION_FILTER_FUNCTIONS, SUGGESTION_SORT_FUNCTIONS
from ..models import db, Suggestion, Tag, User



def get_suggestions(limit: int = None, offset: int = None, filters: str = None, search: str = None, sort: str = 'DEFAULT') -> str:
    """
    Returns all suggestions.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All suggestion matching the query in json format
    """

    def query_func():
        if sort in SUGGESTION_SORT_FUNCTIONS:
            query = SUGGESTION_SORT_FUNCTIONS.get(sort)(db.session)

        if filters and _validate_filters(filters):
            for name, value in filters:
                filter_func = SUGGESTION_FILTER_FUNCTIONS.get(name.upper())
                if filter_func:
                    query = filter_func(query, value.upper())

        if search:
            # Please append more fields, if you'd like to include in search
            # Currently the JSON field search is a bit dumb.
            # Ideally, you would like to search matches in each language separately,
            # instead of the whole json blob (cast as string)
            query = query.filter(or_(
                Suggestion.preferred_label.cast(Unicode).contains(search),
                Suggestion.alternative_labels.cast(Unicode).contains(search),
                Suggestion.description.contains(search),
                Suggestion.reason.contains(search)
            ))

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        return query.all()

    def _validate_filters(f):
        return all([f[0].upper() in SUGGESTION_FILTER_FUNCTIONS.keys() for f in filters])

    if filters:
        # status:accepted|type:new|meeting:12
        # -> [['status', 'accepted'], ['type', 'new'], ['meeting', '12']]
        filters = [f.split(':') for f in filters.split('|')]

    return get_all_or_404_custom(query_func)


def get_user_suggestions(user_id: int) -> str:
    """
    Gets suggestions by user id
    :params user_id
    :returns suggestions or error
    """

    if user_id > 0:
        user_suggestions = Suggestion.query.filter_by(user_id=user_id).all()
        serialized_objects = [o.as_dict() for o in user_suggestions]
        return { 'data': serialized_objects, 'code': 200 }, 200

    return { 'error': 'user_id was not valid', 'code': 400}, 400


def get_suggestion(suggestion_id: int) -> str:
    """
    Returns a suggestion by id.

    :param id: Suggestion id
    :returns: A single suggestion object as json
    """

    return get_one_or_404(Suggestion, suggestion_id)


@suggestion_parameter_validator
def post_suggestion() -> str:
    """
    Creates a single suggestion.

    Request body should include a single suggestion object.
    The object should be validated by Connexion according to the API definition.

    :returns: the created suggestion as json
    """
    created_response = create_or_404(Suggestion, connexion.request.json)
    response = created_response[0]

    if response is not None and response['code'] is 201:
      suggestion_id = response['data']['id']
      protocol = connexion.request.environ['HTTP_X_FORWARDED_PROTO']
      baseurl = connexion.request.environ['HTTP_HOST'].split(',')[1]

      if suggestion_id > 0 and protocol is not '' and baseurl is not None and baseurl is not '':
        response['suggestionUrl'] = f'{protocol}://{baseurl}/suggestions/{suggestion_id}'

    return response

@admin_only
@suggestion_parameter_validator
def put_suggestion(suggestion_id: int) -> str:
    """
    Updates a single suggestion by id.
    Request body should include a single suggestion object.

    :returns: the created suggestion as json
    """
    return update_or_404(Suggestion, suggestion_id, connexion.request.json)


@admin_only
@suggestion_parameter_validator
def patch_suggestion(suggestion_id: int) -> str:
    """
    Updates a single suggestion by id.
    Request body should include a single suggestion object.

    :returns: the created suggestion as json
    """

    return patch_or_404(Suggestion, suggestion_id, connexion.request.json)


@admin_only
def delete_suggestion(suggestion_id: int) -> str:
    """
    Deletes a suggestion by id.

    :param id: Suggestion id
    :returns: 204, No Content on success
    """

    return delete_or_404(Suggestion, suggestion_id)


@admin_only
@suggestion_id_validator
def add_tags_to_suggestion(suggestion_id: int) -> str:
    """
    Adds the given tags to the suggestion.
    New tags are created on the go, if they don't yet exist.

    :returns: the updated suggestion as json
    """

    def _get_or_create_tag(label):
        instance = Tag.query.get(label)
        if not instance:
            instance = Tag(label=label)
            db.session.add(instance)
            db.session.commit()

        return instance

    payload = connexion.request.json

    suggestion = Suggestion.query.get(suggestion_id)
    # Example:
    # { tags: [ 'Tag_1', 'Tag_2', 'Tag_3' ] }
    for label in [label.upper() for label in payload.get('tags')]:
        tag = _get_or_create_tag(label)
        suggestion.tags.append(tag)

    db.session.commit()

    return create_response(suggestion.as_dict(), 201)


@admin_only
@suggestion_id_validator
def remove_tags_from_suggestion(suggestion_id: int) -> str:
    """
    Removes the given tags from the suggestion.

    :param id: Suggestion id
    :returns: 204, No Content on success
    """

    payload = connexion.request.json

    suggestion = Suggestion.query.get(suggestion_id)
    tag_labels_upper = [label.upper() for label in payload.get('tags')]
    tags = db.session.query(Tag).filter(Tag.label.in_(tag_labels_upper)).all()

    # Example:
    # { tags: [ 'Tag_1', 'Tag_2', 'Tag_3' ] }
    for tag in tags:
        if tag in suggestion.tags:
            suggestion.tags.remove(tag)

    db.session.commit()

    return { 'code': 202 }, 202


@admin_only
@suggestion_id_validator
def assign_to_user(suggestion_id: int, user_id: int) -> str:
    user = User.query.get(user_id)
    if not user:
        return create_response({}, 404, _error_messagify(User))
    suggestion = Suggestion.query.get(suggestion_id)
    suggestion.user_id = user_id
    db.session.add(suggestion)
    db.session.commit()
    return create_response(suggestion.as_dict(), 202)


@admin_only
@suggestion_id_validator
def unassign(suggestion_id: int) -> str:
    suggestion = Suggestion.query.get(suggestion_id)
    suggestion.user_id = None
    db.session.add(suggestion)
    db.session.commit()
    return create_response(suggestion.as_dict(), 202)


def get_meeting_suggestions(meeting_id: int) -> str:
    """
    Gets suggestions by meeting id
    :params meeting_id
    :returns suggestions or error
    """

    if meeting_id > 0:
        meeting_suggestions = Suggestion.query.filter_by(meeting_id=meeting_id).all()
        serialized_objects = [o.as_dict() for o in meeting_suggestions]
        return { 'data': serialized_objects, 'code': 200 }, 200

    return { 'error': 'meeting_id was not valid', 'code': 400}, 400


@admin_only
@suggestion_id_validator
def put_update_suggestion_status(suggestion_id: int, status: str) -> str:
    """
    Updates suggestion status info (mainly to ACCEPTED or REJECTED)
    """

    if suggestion_id > 0 and len(status) > 0:
        try:
            suggestion = Suggestion.query.get(suggestion_id)
            suggestion.status = status
            db.session.add(suggestion)
            db.session.commit()
            return { 'code': 202 }, 202
        except Exception as ex:
            db.session.rollback()
            print(str(ex))
            return { 'error': str(ex) }, 400