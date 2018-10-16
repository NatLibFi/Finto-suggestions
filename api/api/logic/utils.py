from sqlalchemy import or_
from ..models import db, Event, Reaction, Suggestion, SuggestionTypes, SuggestionStatusTypes
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


SUGGESTION_FILTER_FUNCTIONS = {
    'STATUS': (
        lambda query, value:
        query.filter(Suggestion.status == SuggestionStatusTypes[value])
        if value in SuggestionStatusTypes.__members__
        else _raise_exception(value, 'STATUS', [e.name for e in SuggestionStatusTypes])
    ),
    'SUGGESTION_TYPE': (
        lambda query, value:
        query.filter(Suggestion.status == SuggestionTypes[value])
        if value in SuggestionTypes.__members__
        else _raise_exception(value, 'SUGGESTION_TYPE', [e.name for e in SuggestionTypes])
    ),
    'MEETING_ID': _meeting_id_filter
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
        .filter(or_(
            Event.event_type == 'COMMENT',
            Event.event_type == None  # pylint: disable=C0121
        ))
        .group_by(Suggestion.id)
        .order_by(
            db.func.count(Event.event_type).desc(),
            Suggestion.created.desc()
        )
    ),
    'COMMENTS_ASC': (
        lambda session:
        session.query(Suggestion)
        .outerjoin(Event)
        .filter(or_(
            Event.event_type == 'COMMENT',
            Event.event_type == None  # pylint: disable=C0121
        ))
        .group_by(Suggestion.id)
        .order_by(
            db.func.count(Event.event_type).asc(),
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
