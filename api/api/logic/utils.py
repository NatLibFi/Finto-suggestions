from sqlalchemy import or_

from ..models import db, Event, Tag, Reaction, Suggestion, SuggestionTypes, SuggestionStatusTypes
from .common import InvalidFilterException


def _raise_exception(value, filter_type, valid_types=None):
    msg = 'Invalid value {} for filter type {}.'.format(
        value, filter_type)
    if valid_types:
        msg += ' valid values: {}'.format(', '.join(valid_types))

    raise InvalidFilterException(msg)

def _meeting_id_filter(query, value):
    if value == 'NULL':
        value = None
    elif value.isdigit():
        value = int(value)
    else:
        _raise_exception(value, 'MEETING')

    return query.filter(Suggestion.meeting_id == value)

def _tags_filter(query, values):
    for value in values.split('\b'):
        query = query.filter(Suggestion.tags.any(Tag.label == value))

    return query

def _user_id_filter(query, value):
    if value == 'NULL':
        value = None
    elif value.isdigit():
        value = int(value)
    else:
        _raise_exception(value, 'USER')

    return query.filter(Suggestion.user_id == value)

SUGGESTION_FILTER_FUNCTIONS = {
    'STATUS': (
        lambda query, value:
        query.filter(Suggestion.status == SuggestionStatusTypes[value])
        if value in SuggestionStatusTypes.__members__
        else _raise_exception(value, 'STATUS', [e.name for e in SuggestionStatusTypes])
    ),
    'TYPE': (
        lambda query, value:
        query.filter(Suggestion.suggestion_type == SuggestionTypes[value])
        if value in SuggestionTypes.__members__
        else _raise_exception(value, 'SUGGESTION_TYPE', [e.name for e in SuggestionTypes])
    ),
    'MEETING_ID': _meeting_id_filter,
    'TAGS': _tags_filter,
    'USER_ID': _user_id_filter
}


SUGGESTION_SORT_FUNCTIONS = {
    'DEFAULT': (lambda session: session.query(Suggestion)),
    'CREATED_DESC': (
        lambda session:
        session.query(Suggestion)
        .order_by(Suggestion.created.desc())
    ),
    'CREATED_ASC': (
        lambda session:
        session.query(Suggestion)
        .order_by(Suggestion.created.asc())
    ),
    'COMMENTS_DESC': (
        lambda session:
        session.query(Suggestion)
        .outerjoin(Event)
        .group_by(Suggestion.id)
        .order_by(
            db.func.count(Event.event_type == "COMMENT").desc(),
            Suggestion.created.desc()
        )
    ),
    'COMMENTS_ASC': (
        lambda session:
        session.query(Suggestion)
        .outerjoin(Event)
        .group_by(Suggestion.id)
        .order_by(
            db.func.count(Event.event_type == "COMMENT").asc(),
            Suggestion.created.desc()
        )
    ),
    'UPDATED_DESC': (
        lambda session:
        session.query(Suggestion)
        .order_by(Suggestion.modified.desc())
    ),
    'REACTIONS_DESC': (
        lambda session:
        session.query(Suggestion)
        .outerjoin(Reaction)
        .group_by(Suggestion.id)
        .order_by(
            db.func.count(Reaction.id).desc(),
            Suggestion.created.desc()
        )
    )
}
