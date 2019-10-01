import os
import connexion
from sqlalchemy import or_, func, and_
from sqlalchemy.types import Unicode
from ..authentication import admin_only
from .validators import suggestion_parameter_validator, suggestion_id_validator, _error_messagify
from .common import (create_response, get_one_or_404, get_all_or_404, get_all_or_404_custom,
                     get_count_or_404_custom, create_or_400, delete_or_404, patch_or_404, update_or_404)
from .utils import SUGGESTION_FILTER_FUNCTIONS, SUGGESTION_SORT_FUNCTIONS
from ..models import db, Suggestion, Tag, User
from .skos import initGraph, suggestionToGraph
from flask import jsonify
from rdflib import Graph, URIRef, Literal, Namespace, RDF
from rdflib.namespace import SKOS

from ..tools.profiler import profiler
import json
import logging

# Profiler decorator, enable if needed
# @profiler
def get_suggestions(limit: int = None, offset: int = None, filters: str = None, search: str = None, sort: str = 'DEFAULT') -> str:
    """
    Returns all suggestions.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :param filters: Filter the results based on filter selections
    :param search: Filter the results based on search word
    :param sort: Sort the results before returning them
    :returns: All suggestion matching the query in json format
    """

    def query_func():
        if sort in SUGGESTION_SORT_FUNCTIONS:
            query = SUGGESTION_SORT_FUNCTIONS.get(sort)(db.session)
        else:
            query = SUGGESTION_SORT_FUNCTIONS.get('CREATED_DESC')(db.session)

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
                func.lower(Suggestion.preferred_label.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.alternative_labels.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.description).contains(search.lower()),
                func.lower(Suggestion.reason).contains(search.lower()),
                func.lower(Suggestion.uri).contains(search.lower()),
                func.lower(Suggestion.organization).contains(search.lower()),
                func.lower(Suggestion.broader_labels.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.narrower_labels.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.related_labels.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.groups.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.scopeNote).contains(search.lower()),
                func.lower(Suggestion.exactMatches.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.neededFor).contains(search.lower()),
                func.lower(Suggestion.yse_term.cast(Unicode)).contains(search.lower()),
            ))

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        return query.all()

    def _validate_filters(f):
        return all([f[0].upper() in SUGGESTION_FILTER_FUNCTIONS.keys() for f in filters])

    if filters:
        # status:accepted|type:new|meeting_id:12|tags:melinda-slm|user_id:1
        # -> [['status', 'accepted'], ['type', 'new'], ['meeting_id', '12'], ['tags', 'melinda-slm'], ['user_id', '1]]
        filters = [f.split(':') for f in filters.split('|')]

    return get_all_or_404_custom(query_func)


def get_suggestions_count(filters: str = None, search: str = None) -> str:
    """
    Returns the amount of suggestions for pagination purposes.

    As the request query can be limited with additional parameters, we take those into account.

    :param filters: Filter the results based on filter selections
    :param search: Filter the results based on search word
    :returns: All suggestion matching the query in json format
    """

    def query_func():
        query = db.session.query(Suggestion)

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
                func.lower(Suggestion.preferred_label.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.alternative_labels.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.description).contains(search.lower()),
                func.lower(Suggestion.reason).contains(search.lower()),
                func.lower(Suggestion.uri).contains(search.lower()),
                func.lower(Suggestion.organization).contains(search.lower()),
                func.lower(Suggestion.broader_labels.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.narrower_labels.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.related_labels.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.groups.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.scopeNote).contains(search.lower()),
                func.lower(Suggestion.exactMatches.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.neededFor).contains(search.lower()),
                func.lower(Suggestion.yse_term.cast(Unicode)).contains(search.lower()),
            ))

        return query.count()

    def _validate_filters(f):
        return all([f[0].upper() in SUGGESTION_FILTER_FUNCTIONS.keys() for f in filters])

    if filters:
        # status:accepted|type:new|meeting:12
        # -> [['status', 'accepted'], ['type', 'new'], ['meeting', '12']]
        filters = [f.split(':') for f in filters.split('|')]

    return get_count_or_404_custom(query_func)

def get_user_suggestions(user_id: int, limit: int = None, offset: int = None) -> str:
    """
    Gets suggestions by user id
    :params user_id
    :returns suggestions or error
    """

    if user_id > 0:
        query = Suggestion.query.filter_by(user_id=user_id).order_by(Suggestion.created.desc())
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        user_suggestions = query.all()
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


def post_suggestion() -> str:
    """
    Creates a single suggestion.

    Request body should include a single suggestion object.
    The object should be validated by Connexion according to the API definition.

    :returns: the created suggestion as json
    """

    def _get_or_create_tag(label):
        instance = Tag.query.get(label)
        if not instance:
            instance = Tag(label=label)
            db.session.add(instance)
            db.session.commit()

        return instance

    payload_dict = connexion.request.json
    payload_dict['status'] = 'RECEIVED'

    # cannot add tags directly – we handle tags separately
    if 'tags' in payload_dict:
        payload_tags = payload_dict['tags']
        payload_dict['tags'] = []

    created_response = create_or_400(Suggestion, payload_dict)
    response = created_response[0]

    if response is not None and response['code'] is 201 and 'tags' in payload_dict and len(payload_tags) > 0:
        suggestion = Suggestion.query.get(response['data']['id'])
        for tag in payload_tags:
            existing_tag = _get_or_create_tag(tag['label'])
            suggestion.tags.append(existing_tag)
            response['data']['tags'].append(tag['label'])

        db.session.commit()

    if response is not None and response['code'] is 201:
        suggestion_id = response['data']['id']
        protocol = connexion.request.environ['HTTP_X_FORWARDED_PROTO']
        baseurl = connexion.request.environ['HTTP_HOST'].split(',')[1]

        if suggestion_id > 0 and protocol is not '' and baseurl is not None and baseurl is not '':
            response['data']['suggestionUrl'] = f'{protocol}://{baseurl}/suggestion/{suggestion_id}'

        return jsonify(response['data']), 201

    else:
        return {'error': 'Could not create suggestion.'}, 400


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
            instance = Tag(label=label, color='#4794a2')
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
    Updates suggestion status info (mainly to ACCEPTED or RETAINED)
    """

    if suggestion_id > 0 and len(status) > 0:
        try:
            suggestion = Suggestion.query.get(suggestion_id)
            suggestion.status = status
            db.session.add(suggestion)
            # Mika 011019
            db.session.commit()
            return { 'code': 202 }, 202
        except Exception as ex:
            db.session.rollback()
            print(str(ex))
            return { 'error': str(ex) }, 400
        


def get_open_suggestions() -> str:
    """
    Get open status suggestions from db
    :returns: Suggestions list of open suggestions
    """
    try:
        open_suggestions = Suggestion.query.filter(Suggestion.status.notin_(['ACCEPTED', 'REJECTED', 'RETAINED', 'ARCHIVED'])).all()
        serialized_objects = [o.as_dict() for o in open_suggestions]
        return { 'data': serialized_objects, 'code': 200 }, 200
    except Exception as ex:
        print(str(ex))
        return { 'code': 404, 'error': str(ex) }, 404


def get_resolved_suggestions() -> str:
    """
    Get open status suggestions from db
    :returns: Suggestions list of resolved suggestions
    """
    try:
        resolved_suggestions = Suggestion.query.filter(Suggestion.status.in_(['ACCEPTED', 'REJECTED', 'RETAINED', 'ARCHIVED'])).all()
        serialized_objects = [o.as_dict() for o in resolved_suggestions]
        return { 'data': serialized_objects, 'code': 200 }, 200
    except Exception as ex:
        print(str(ex))
        return { 'code': 404, 'error': str(ex) }, 404

def get_open_suggestions_skos() -> str:
    """
    Get open status suggestions from db
    :returns: Suggestions list of open suggestions in skos format
    """
    try:
        open_suggestions = Suggestion.query.filter(and_(Suggestion.status.notin_(['ACCEPTED', 'REJECTED', 'RETAINED', 'ARCHIVED']), Suggestion.yse_term["url"] == None)).all()
        graph = None
        for suggestion in open_suggestions:
            graph = suggestionToGraph(suggestion.as_dict(), graph)
        try:
            return graph.serialize(format='turtle')
        except Exception as ex:
            print(str(ex))

    except Exception as ex:
        print(str(ex))
        return { 'code': 404, 'error': str(ex) }, 404


def get_suggestion_skos(suggestion_id: int) -> str:
    """
    Returns a suggestion by id in skos format.

    :param id: Suggestion id
    :returns: A single suggestion object as json
    """

    try:
        suggestion = Suggestion.query.filter_by(id=suggestion_id).first()
        graph = suggestionToGraph(suggestion.as_dict())
        try:
            return graph.serialize(format='turtle')
        except Exception as ex:
            print(str(ex))
    except Exception as ex:
        print(str(ex))
        return { 'code': 404, 'error': str(ex) }, 404

