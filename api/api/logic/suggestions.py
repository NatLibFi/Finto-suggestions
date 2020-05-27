import connexion
from flask import jsonify
from sqlalchemy import or_, func, and_, Table, Column, String, MetaData, literal, select
from sqlalchemy.types import Unicode

from ..authentication import admin_only
from .validators import suggestion_parameter_validator, suggestion_id_validator, _error_messagify
# pylint: disable=unused-import
from .common import (create_response, get_one_or_404, get_all_or_400, get_all_or_400_custom,
                     get_count_or_400_custom, create_or_400, delete_or_404, patch_or_404, update_or_404)
# pylint: enable=unused-import
from .utils import SUGGESTION_FILTER_FUNCTIONS, SUGGESTION_SORT_FUNCTIONS
from ..models import db, Suggestion, Tag, User, Event
from .skos import suggestionToGraph

# Profiler decorator, enable if needed
# @profiler


def getQuery(limit: int = 0, offset: int = 0, filters: str = "", queryString: str = "", sort: str = 'DEFAULT') -> db.Query:
    """
    Returns query for querying all suggestions.

    Query can be sorted and limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :param filters: Filter the results based on filter selections
    :param queryString: Filter the results based on search term
    :param sort: Sort the result set
    :returns: Query object for querying the database
    """
    isTitleSet = False

    sort = sort.upper()
    if sort not in SUGGESTION_SORT_FUNCTIONS:
        sort = "CREATED_DESC"

    query = SUGGESTION_SORT_FUNCTIONS.get(sort)(db.session)

    if filters:
        filters = [f.split(':') for f in filters.strip('|').split('|')]
        for name, value in filters:
            filter_func = SUGGESTION_FILTER_FUNCTIONS.get(name.upper(), None)
            if filter_func:
                query = filter_func(query, value.upper())
            else:
                # Could not find appropriate filter, skip it
                pass

    queryString = queryString.lower()
    if queryString:
        queryStringForAllFileds = queryString
        if 'title:' in queryString:
            isTitleSet = True
            queryStringForOnlytTitlesSearch = queryString.replace('title:', '')

        if isTitleSet is True:
            query = query.filter(or_(
                func.lower(Suggestion.preferred_label['fi']['value'].cast(
                    Unicode)).contains(queryStringForOnlytTitlesSearch),
                func.lower(Suggestion.preferred_label['sv'].cast(
                    Unicode)).contains(queryStringForOnlytTitlesSearch),
                func.lower(Suggestion.preferred_label['en'].cast(
                    Unicode)).contains(queryStringForOnlytTitlesSearch),
                func.lower(Suggestion.id.cast(Unicode)).contains(queryStringForOnlytTitlesSearch),
            ))
        else:
            query = query.filter(or_(
                func.lower(Suggestion.preferred_label['fi']['value'].cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.preferred_label['sv'].cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.preferred_label['en'].cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.id.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.description.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.reason.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.uri.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.organization.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.broader_labels.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.narrower_labels.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.related_labels.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.groups.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.scopeNote.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.exactMatches.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.neededFor.cast(
                    Unicode)).contains(queryStringForAllFileds),
                func.lower(Suggestion.yse_term.cast(
                    Unicode)).contains(queryStringForAllFileds),
            ))

    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)

    return query


def getTestQuery(model: object) -> db.Query:
    """
    Returns query for querying all suggestions.

    Query can be sorted and limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :param filters: Filter the results based on filter selections
    :param queryString: Filter the results based on search term
    :param sort: Sort the result set
    :returns: Query object for querying the database
    """
    # , limit: int = 0, offset: int = 0
    # query = SUGGESTION_SORT_FUNCTIONS.get('CREATED_DESC')(db.session)
    # query = query.get(4321)
    #  filter(or_(func(Suggestion.preferred_label['fi']['value'].cast(Unicode)), func(Suggestion.id.cast(Unicode))))
    # print("OOOOOOOOOOOOOOOOOOOOOOOOOOO")
    # print(query)

        #     query = query.filter(or_(
        #         func.lower(Suggestion.preferred_label['fi']['value'].cast(
        #             Unicode)).contains(queryStringForOnlytTitlesSearch),
        #         func.lower(Suggestion.preferred_label['sv'].cast(
        #             Unicode)).contains(queryStringForOnlytTitlesSearch),
        #         func.lower(Suggestion.preferred_label['en'].cast(
        #             Unicode)).contains(queryStringForOnlytTitlesSearch),
        #         func.lower(Suggestion.id.cast(Unicode)).contains(queryStringForOnlytTitlesSearch),
        #     ))
        # else:


    # if limit:
    #     query = query.limit(limit)
    # if offset:
    #     query = query.offset(offset)

    return db.Query

def get_suggestions(limit: int = 0, offset: int = 0, filters: str = "", search: str = "", sort: str = 'DEFAULT') -> str:
    """
    Returns all suggestions.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :param filters: Filter the results based on filter selections
    :param search: Filter the results based on search term
    :param sort: Sort the results before returning them
    :returns: All suggestion matching the query in json format
    """

    # print("*************************************")
    # queryTest = getTestQuery(Event)
    # print(queryTest)
    # # get_all_or_400_custom(queryTest)
    # # bigQuery = get_all_or_400_custom(queryTest)
    # # print(bigQuery)
    # print("*************************************")

    query = getQuery(limit=limit, offset=offset, filters=filters, queryString=search, sort=sort)

    return  get_all_or_400_custom(query)


def get_suggestions_count(filters: str = "", search: str = "") -> str:
    """
    Returns the amount of suggestions for pagination purposes.

    As the request query can be limited with additional parameters, we take those into account.

    :param filters: Filter the results based on filter selections
    :param search: Filter the results based on search term
    :returns: All suggestion matching the query in json format
    """

    query = getQuery(filters=filters, queryString=search)
    return get_count_or_400_custom(query)


def get_archived_suggestions_count(filters: str = "", search: str = "") -> str:
    """
    Returns the amount of archived suggestions.

    As the request query can be limited with additional parameters, we take those into account.

    :param filters: Filter the results based on filter selections
    :param search: Filter the results based on search term
    :returns: The amount of archived suggestions matching the query.
    """
    if "status:archived" not in filters:
        filters = "status:archived|" + filters

    query = getQuery(filters=filters, queryString=search)
    return get_count_or_400_custom(query)


def get_user_suggestions(user_id: int, limit: int = None, offset: int = None) -> str:
    """
    Gets suggestions by user id
    :params user_id
    :returns suggestions or error
    """

    if user_id > 0:
        query = Suggestion.query.filter_by(
            user_id=user_id).order_by(Suggestion.created.desc())
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        user_suggestions = query.all()
        serialized_objects = [o.as_dict() for o in user_suggestions]
        return {'data': serialized_objects, 'code': 200}, 200

    return {'error': 'user_id was not valid', 'code': 400}, 400


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

    if 'broader_labels' not in payload_dict:
        payload_dict['broader_labels'] = []

    if 'exactMatches' not in payload_dict:
        payload_dict['exactMatches'] = []

    if 'groups' not in payload_dict:
        payload_dict['groups'] = []

    if 'narrower_labels' not in payload_dict:
        payload_dict['narrower_labels'] = []

    if 'related_labels' not in payload_dict:
        payload_dict['related_labels'] = []

    if 'alternative_labels' not in payload_dict:
        payload_dict['alternative_labels'] = []

    created_response = create_or_400(Suggestion, payload_dict)
    response = created_response[0]

    if response is not None and response['code'] == 201 and 'tags' in payload_dict and len(payload_tags) > 0:
        suggestion = Suggestion.query.get(response['data']['id'])
        for tag in payload_tags:
            existing_tag = _get_or_create_tag(tag['label'])
            suggestion.tags.append(existing_tag)
            response['data']['tags'].append(tag['label'])

        db.session.commit()

    if response is not None and response['code'] == 201:
        suggestion_id = response['data']['id']
        protocol = connexion.request.environ['HTTP_X_FORWARDED_PROTO']
        baseurl = connexion.request.environ['HTTP_HOST'].split(',')[1]

        if suggestion_id > 0 and protocol != '' and baseurl is not None and baseurl != '':
            response['data']['suggestionUrl'] = f'{protocol}://{baseurl}/suggestion/{suggestion_id}'

        return jsonify(response['data']), 201

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

    return {'code': 202}, 202


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
        meeting_suggestions = Suggestion.query.filter_by(
            meeting_id=meeting_id).all()
        serialized_objects = [o.as_dict() for o in meeting_suggestions]
        return {'data': serialized_objects, 'code': 200}, 200

    return {'error': 'meeting_id was not valid', 'code': 400}, 400


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
            db.session.commit()
            return {'code': 202}, 202
        except Exception as ex:
            db.session.rollback()
            print(str(ex))
            return {'error': str(ex)}, 400


def get_open_suggestions() -> str:
    """
    Get open status suggestions from db
    :returns: Suggestions list of open suggestions
    """
    try:
        open_suggestions = Suggestion.query.filter(Suggestion.status.notin_(
            ['ACCEPTED', 'REJECTED', 'ARCHIVED'])).all()
        serialized_objects = [o.as_dict() for o in open_suggestions]
        return {'data': serialized_objects, 'code': 200}, 200
    except Exception as ex:
        print(str(ex))
        return {'code': 404, 'error': str(ex)}, 404


def get_resolved_suggestions() -> str:
    """
    Get open status suggestions from db
    :returns: Suggestions list of resolved suggestions
    """
    try:
        resolved_suggestions = Suggestion.query.filter(Suggestion.status.in_(
            ['ACCEPTED', 'REJECTED', 'RETAINED', 'ARCHIVED'])).all()
        serialized_objects = [o.as_dict() for o in resolved_suggestions]
        return {'data': serialized_objects, 'code': 200}, 200
    except Exception as ex:
        print(str(ex))
        return {'code': 404, 'error': str(ex)}, 404


def get_open_suggestions_skos() -> str:
    """
    Get open status suggestions from db
    :returns: Suggestions list of open suggestions in skos format
    """
    try:
        open_suggestions = Suggestion.query.filter(and_(Suggestion.status.notin_(
            ['ACCEPTED', 'REJECTED', 'ARCHIVED']), Suggestion.yse_term["url"] == None)).all()
        if len(open_suggestions) == 0:
            return {'code': 204, 'message': "No open suggestions"}, 204
        graph = None
        for suggestion in open_suggestions:
            graph = suggestionToGraph(suggestion.as_dict(), graph)
        try:
            return graph.serialize(format='turtle')
        except Exception as ex:
            return {'code': 500, 'error': "Failed to serialize open suggestions"}, 500

    except Exception as ex:
        return {'code': 500, 'error': str(ex)}, 500


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
            return {'code': 500, 'error': "Failed to serialize suggestion"}, 500
    except Exception as ex:
        print(str(ex))
        return {'code': 404, 'error': str(ex)}, 404


def get_suggestion_skosfilter(filters: str = "") -> str:
    '''
    curl -X GET --header 'Accept: text/turtle' --header 'Authorization: Bearer ..YourSHAorSomethingForAuthorization.. '
    'http://localhost:8080/api/suggestions/skosfilter
    ?filters=status:received.read.accepted.rejected.retained.archived|exclude:true/false|type:new/modify/both|
    yse:true/false/both|model:skos/dc/foaf|format:turtle/jsonld/xml/n3/ntriples|
    suggestion_id:0/suggestion_id:nnnn'

    1) At least one status flag should be used
    2) Status flags must be delimited by a dot (.)
    3) The 'pipe' is used as delimiter for query parameters
    4) suggestion_id:0 returns all the filtered suggestions
    5) suggestion_id:nnnn returns only one suggestion by suggestion id
    6) suggestion_id must be the last defined parameter
    7) All the parameters must be defined in the query


    Example:

    curl -X GET --header 'Accept: text/turtle' --header 'Authorization: Bearer ABC123ABC123'
    'http://localhost:8080/api/suggestions/skosfilter?filters=status:received.read.accepted.rejected.retained.archived
    |exclude:false|type:both|yse:both|model:skos|format:turtle|suggestion_id:0'
    '''

    def validFilters():
        amountOfParametersCount = 0  # Cheks the minimums, must be 7
        amountOfParameterOptionsCount = 0  # Cheks the minimums, must be 6
        listOfMandatoryParameters = ['status:', 'exclude:', 'type:', 'yse:', 'model:', 'format:', 'suggestion_id:']
        listOfMandatoryParameterOptions = [
            'status:received', 'status:read', 'status:accepted', 'status:rejected', 'status:retained', 'status:archived',
            'exclude:true', 'exclude:false',
            'type:new', 'type:modify', 'type:both',
            'yse:true', 'yse:false', 'yse:both',
            'model:skos', 'model:dc', 'model:foaf',
            'format:turtle', 'format:jsonld', 'format:xml', 'format:n3', 'format:ntriples'
        ]

        for parameterKey in listOfMandatoryParameters:
            if parameterKey in filters:
                amountOfParametersCount += 1
            else:
                print(f"ParameterKey {parameterKey} is not in querystring")
        for parameterKey in listOfMandatoryParameterOptions:
            if parameterKey in filters:
                amountOfParameterOptionsCount += 1
            else:
                print(f"ParameterKey {parameterKey} is not in querystring")

        return amountOfParametersCount == 7 and amountOfParameterOptionsCount == 6

    def getYse() -> str:
        if "suggestion_id:0" in filters:
            if "yse:true" in filters:
                return 'InYSE'
            if "yse:false" in filters:
                return 'NotInYSE'
            return 'both'
        print("Please, check the passed arguments")
        return ""

    def getSuggestionTypes() -> list:
        if "type:new" in filters:
            return ['NEW']
        if "type:modify" in filters:
            return ['MODIFY']
        if "type:both" in filters:
            return ['NEW', 'MODIFY']
        return ['NEW', 'MODIFY']

    def getFormat() -> str:
        # Serialization formats
        # Turtle, at the moment JSON-LD and XML in use
        if "format:turtle" in filters:
            return 'turtle'
        if "format:jsonld" in filters:
            return 'json-ld'
        if "format:xml" in filters:
            return 'xml'
        if "format:n3" in filters:
            return 'n3'
        if "format:ntriples" in filters:
            return 'turtle'
        return 'turtle'

    def getModel() -> str:
        # Only skos in use at the moment. In the future DC and FOAF will be on the list
        if "model:skos" in filters:
            return 'skos'
        if "model:dc" in filters:
            return 'skos'
        if "model:foaf" in filters:
            return 'skos'
        return 'skos'

    if not validFilters():
        return {'code': 400, 'error': "Invalid filters"}, 400

    inYSE = getYse()
    excluded = "exclude:true" in filters

    returnFormat = getFormat()
    splittedFilters = [f.split(':') for f in filters.split('|')]
    statusList = splittedFilters[0]
    statusValues = statusList[1]
    statusValuesList = statusValues.split('.')
    upperCaseStatusValuesList = [item.upper() for item in statusValuesList]
    filterClauses = []

    if excluded:
        filterClauses.append(Suggestion.status.notin_(upperCaseStatusValuesList))
    else:
        filterClauses.append(Suggestion.status.in_(upperCaseStatusValuesList))

    filterClauses.append(Suggestion.suggestion_type.in_(getSuggestionTypes()))

    if inYSE == 'InYSE':
        filterClauses.append(Suggestion.yse_term["url"] != None)
    elif inYSE == 'NotInYSE':
        filterClauses.append(Suggestion.yse_term["url"] == None)

    try:
        if "suggestion_id:0" not in filters:
            open_suggestions = [Suggestion.query.filter_by(id=filters.split("suggestion_id:", 1)[1]).first()]
        else:
            open_suggestions = Suggestion.query.filter(
                and_(
                    *filterClauses
                )
            ).all()
    except Exception as ex:
        print(str(ex))
        return {'code': 400, 'error': str(ex)}, 400

    if len(open_suggestions) == 0 or open_suggestions[0] is None:
        # Empty result set
        return {'code': 204, 'message': "Empty result set"}, 204

    graph = None
    for suggestion in open_suggestions:
        graph = suggestionToGraph(suggestion.as_dict(), graph)
    try:
        return graph.serialize(format=returnFormat)
    except Exception as ex:
        return {'code': 500, 'error': "Failed to serialize open suggestions"}, 500
