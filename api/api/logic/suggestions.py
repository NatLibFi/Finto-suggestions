import connexion
from flask import jsonify
from sqlalchemy import or_, func, and_
from sqlalchemy.types import Unicode

from ..authentication import admin_only
from .validators import suggestion_parameter_validator, suggestion_id_validator, _error_messagify
# pylint: disable=unused-import
from .common import (create_response, get_one_or_404, get_all_or_404, get_all_or_404_custom,
                     get_count_or_404_custom, create_or_400, delete_or_404, patch_or_404, update_or_404)
# pylint: enable=unused-import
from .utils import SUGGESTION_FILTER_FUNCTIONS, SUGGESTION_SORT_FUNCTIONS
from ..models import db, Suggestion, Tag, User
from .skos import suggestionToGraph

# Profiler decorator, enable if needed
# @profiler
def get_suggestions(limit: int = 0, offset: int = 0, filters: str = "", search: str = "", sort: str = 'DEFAULT') -> str:
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
                func.lower(Suggestion.preferred_label['fi']['value'].cast(
                    Unicode)).contains(search.lower()),
                func.lower(Suggestion.preferred_label['sv'].cast(
                    Unicode)).contains(search.lower()),
                func.lower(Suggestion.preferred_label['en'].cast(
                    Unicode)).contains(search.lower()),
                # func.lower(Suggestion.alternative_labels.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.id.cast(Unicode)).contains(search),
                # func.lower(Suggestion.description).contains(search.lower()),
                # func.lower(Suggestion.reason).contains(search.lower()),
                # func.lower(Suggestion.uri).contains(search.lower()),
                # func.lower(Suggestion.organization).contains(search.lower()),
                # func.lower(Suggestion.broader_labels.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.narrower_labels.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.related_labels.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.groups.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.scopeNote).contains(search.lower()),
                # func.lower(Suggestion.exactMatches.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.neededFor).contains(search.lower()),
                # func.lower(Suggestion.yse_term.cast(Unicode)).contains(search.lower()),
            ))

        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        return query.all()

    def _validate_filters(filters):
        return all([filter[0].upper() in SUGGESTION_FILTER_FUNCTIONS.keys() for filter in filters])

    if filters:
        # status:accepted|type:new|meeting_id:12|tags:melinda-slm|user_id:1
        # -> [['status', 'accepted'], ['type', 'new'], ['meeting_id', '12'], ['tags', 'melinda-slm'], ['user_id', '1]]
        filters = [f.split(':') for f in filters.split('|')]

    return get_all_or_404_custom(query_func)


def get_suggestions_count(filters: str = "", search: str = "") -> str:
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
                func.lower(Suggestion.preferred_label['fi']['value'].cast(
                    Unicode)).contains(search.lower()),
                func.lower(Suggestion.preferred_label['sv'].cast(
                    Unicode)).contains(search.lower()),
                func.lower(Suggestion.preferred_label['en'].cast(
                    Unicode)).contains(search.lower()),
                # func.lower(Suggestion.alternative_labels.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.id.cast(Unicode)).contains(search),
                # func.lower(Suggestion.description).contains(search.lower()),
                # func.lower(Suggestion.reason).contains(search.lower()),
                # func.lower(Suggestion.uri).contains(search.lower()),
                # func.lower(Suggestion.organization).contains(search.lower()),
                # func.lower(Suggestion.broader_labels.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.narrower_labels.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.related_labels.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.groups.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.scopeNote).contains(search.lower()),
                # func.lower(Suggestion.exactMatches.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.neededFor).contains(search.lower()),
                # func.lower(Suggestion.yse_term.cast(Unicode)).contains(search.lower()),
            ))

        return query.count()

    def _validate_filters(filters):
        return all([filter[0].upper() in SUGGESTION_FILTER_FUNCTIONS.keys() for filter in filters])

    if filters:
        # status:accepted|type:new|meeting:12
        # -> [['status', 'accepted'], ['type', 'new'], ['meeting', '12']]
        filters = [f.split(':') for f in filters.split('|')]

    return get_count_or_404_custom(query_func)


def get_archived_suggestions_count(filters: str = "", search: str = "") -> str:
    """
    Returns the amount of archived suggestions.

    As the request query can be limited with additional parameters, we take those into account.

    :param filters: Filter the results based on filter selections
    :param search: Filter the results based on search word
    :returns: The amount of archived suggestions matching the query.
    """
    if "status:archived" not in filters:
        filters = "status:archived|" + filters

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
                func.lower(Suggestion.preferred_label['fi']['value'].cast(
                    Unicode)).contains(search.lower()),
                # func.lower(Suggestion.preferred_label.cast(Unicode)).contains(search.lower()),

                func.lower(Suggestion.preferred_label['sv'].cast(
                    Unicode)).contains(search.lower()),
                func.lower(Suggestion.preferred_label['en'].cast(
                    Unicode)).contains(search.lower()),
                # func.lower(Suggestion.alternative_labels.cast(Unicode)).contains(search.lower()),
                func.lower(Suggestion.id.cast(Unicode)).contains(search),
                # func.lower(Suggestion.description).contains(search.lower()),
                # func.lower(Suggestion.reason).contains(search.lower()),
                # func.lower(Suggestion.uri).contains(search.lower()),
                # func.lower(Suggestion.organization).contains(search.lower()),
                # func.lower(Suggestion.broader_labels.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.narrower_labels.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.related_labels.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.groups.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.scopeNote).contains(search.lower()),
                # func.lower(Suggestion.exactMatches.cast(Unicode)).contains(search.lower()),
                # func.lower(Suggestion.neededFor).contains(search.lower()),
                # func.lower(Suggestion.yse_term.cast(Unicode)).contains(search.lower()),
            ))

        return query.count()

    def _validate_filters(filters):
        return all([filter[0].upper() in SUGGESTION_FILTER_FUNCTIONS.keys() for filter in filters])

    if filters and len(filters) > 0:
        # status:accepted|type:new|meeting:12
        # -> [['status', 'accepted'], ['type', 'new'], ['meeting', '12']]
        filters = [f.split(':') for f in filters.split('|') if len(f) > 0]

    return get_count_or_404_custom(query_func)


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

    # Mika's test area for getting missing lists inserted into the db with at least brackets
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

        print("#### Response: " + str(jsonify(response['data'])))
        return jsonify(response['data']), 201

    else:
        print("#### Response: " + str(jsonify(response['data']))) 
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
            # Mika 011019
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
# def get_open_suggestions_skos(search_terms: str) -> str:

    """
    Get open status suggestions from db
    :returns: Suggestions list of open suggestions in skos format
    """
        #   description: 'Pipe-separated filter string, i.e. status:accepted|type:new|meeting_id:12'


    # def _validate_filters(filters):
    #     return all([filter[0].upper() in SUGGESTION_FILTER_FUNCTIONS.keys() for filter in filters])

    # if filters:
    #     # status:accepted|type:new|meeting_id:12|tags:melinda-slm|user_id:1
    #     # -> [['status', 'accepted'], ['type', 'new'], ['meeting_id', '12'], ['tags', 'melinda-slm'], ['user_id', '1]]
    #     filters = [f.split(':') for f in filters.split('|')]

    # return get_all_or_404_custom(query_func)

##Start
    # if search_terms:
    #     print(search_terms)
    # status:accepted|type:new|meeting:12
    # -> [['status', 'accepted'], ['type', 'new'], ['meeting', '12']]
    # filters = [f.split(':') for f in filters.split('|')]
    # try:
    #     suggestion = Suggestion.query.filter_by(id=suggestion_id).first()
    #     graph = suggestionToGraph(suggestion.as_dict())
    #     try:
    #         return graph.serialize(format='turtle')
    #     except Exception as ex:
    #         print(str(ex))
    # except Exception as ex:
    #     print(str(ex))
    #     return {'code': 404, 'error': str(ex)}, 404
        # return search_terms




# return get_count_or_404_custom(query_func)
#End



#   tekstiä
#   tekstiä  

#original start

    try:
        open_suggestions = Suggestion.query.filter(and_(Suggestion.status.notin_(
            ['ACCEPTED', 'REJECTED', 'ARCHIVED']), Suggestion.yse_term["url"] == None)).all()
        graph = None
        for suggestion in open_suggestions:
            graph = suggestionToGraph(suggestion.as_dict(), graph)
        try:
            return graph.serialize(format='turtle')
        except Exception as ex:
            print(str(ex))

    except Exception as ex:
        print(str(ex))
        return {'code': 404, 'error': str(ex)}, 404

#original ends


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
        return {'code': 404, 'error': str(ex)}, 404

def get_suggestion_skosjoku(filters: str = "") -> str:

    '''
    curl -X GET --header 'Accept: text/turtle' --header 'Authorization: Bearer ..YourSHAorSomethingForAuthorization.. ' 
    'http://localhost:8080/api/suggestions/skosjoku
    ?filters=status:received.read.accepted.rejected.retained.archived|exclude:true/false|type:new/modify/both|
    yse:true/false/both|model:skos/dc/foaf|format:turtle/jsonld/xml/n3/ntriples|
    suggestion_id:0/suggestion_id:nnnn'

    1) At least one status flag should be used
    2) Status flags must be delimited by a dot (.)
    3) The 'pipe' is used as delimiter for query parameters 
    4) suggestion_id:0 returns all the filtered suggestions
    5) suggestion_id:nnnn retruns only one suggestion by suggestion id
    6) All the parameters must be defined in the query


    Example:

    curl -X GET --header 'Accept: text/turtle' --header 'Authorization: Bearer ABC123ABC123'
    'http://localhost:8080/api/suggestions/skosjoku?filters=status:received.read.accepted.rejected.retained.archived
    |exclude:false|type:both|yse:both|model:skos|format:turtle|suggestion_id:0'
    '''
    print("Before validation")
    print(filters)

    def validateQueryParameters(filters: str = ""):
        amountOfParametersCount = 0 # Cheks the minimums, must be 7
        amountOfParameterOptionsCount = 0 # Cheks the minimums, must be 6
        listOfMandatoryParameters = ['status:', 'exclude:', 'type:', 'yse:', 'model:', 'format:', 'suggestion_id:']
        listOfMandatoryParameterOptions = ['status:received', 'status:read', 'status:accepted', 'status:rejected' 'status:retained',\
            'status:archived', 'exclude:true', 'exclude:false', 'type:new', 'type:modify', 'type:both', 'yse:true', 'yse:false',\
                'yse:both', 'model:skos', 'model:dc', 'model:foaf', 'format:turtle', 'format:jsonld', 'format:xml', 'format:n3',\
                     'format:ntriples']
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

        if amountOfParametersCount == 7 and amountOfParameterOptionsCount == 6:
            return True
        else:
            return False

    inYSE = ''
    tempId = ''
    ifItIsExcluded = False

    def conditionsForSuggestionTypes(filters: str = "") -> list:
        if "type:new" in filters:
            return ['NEW']
        elif "type:modify" in filters:
            return ['MODIFY']
        elif "type:both" in filters:
            return ['NEW', 'MODIFY']
        else:
            print("Type of suggestions is not set")

    def formatInUse(filters: str = "") -> str:
        # Serialization formats
        # Turtle, at the moment JSON-LD and XML in use
        if "format:turtle" in filters:
            return 'turtle'
        elif "format:jsonld" in filters:
            return 'json-ld'
        elif "format:xml" in filters:
            return 'xml'
        elif "format:n3" in filters:
            return 'n3'
        elif "format:ntriples" in filters:
            return 'turtle'
        else:
            return 'turtle'

    def modelInUse(filters: str = "") -> str:
        # Only skos in use at the moment. In the future DC and FOAF will be on the list
        if "model:skos" in filters:
            return 'skos'
        elif "model:dc" in filters:
            return 'skos'
        elif "model:foaf" in filters:
            return 'skos'
        else:
            return 'skos'

    if len(filters) > 0 and validateQueryParameters(filters) == True:
        if "exclude:true" in filters:
            ifItIsExcluded = True
        else:
            print("An inclusive search in use")

        if "suggestion_id:0" in filters:
            if "yse:true" in filters:
                inYSE = 'InYSE'
            elif "yse:false" in filters:
                inYSE = 'NotInYSE'
            else:
                inYSE = 'both'

            splittedFilters = [f.split(':') for f in filters.split('|')]
            statusList = splittedFilters[0]
            statusValues = statusList[1]
            statusValuesList = statusValues.split('.')
            upperCaseStatusValuesList = [item.upper() for item in statusValuesList]

            try:
                if inYSE == 'InYSE':
                    if ifItIsExcluded:
                        open_suggestions = Suggestion.query.filter(and_(Suggestion.status.notin_(
                        upperCaseStatusValuesList), Suggestion.suggestion_type.in_(conditionsForSuggestionTypes(filters)),\
                             Suggestion.yse_term["url"] != None)).all()
                    else:
                        open_suggestions = Suggestion.query.filter(and_(Suggestion.status.in_(
                        upperCaseStatusValuesList), Suggestion.suggestion_type.in_(conditionsForSuggestionTypes(filters)),\
                             Suggestion.yse_term["url"] != None)).all()
                elif inYSE == 'NotInYSE':
                    if ifItIsExcluded:
                        open_suggestions = Suggestion.query.filter(and_(Suggestion.status.notin_(
                        upperCaseStatusValuesList), Suggestion.suggestion_type.in_(conditionsForSuggestionTypes(filters)),\
                             Suggestion.yse_term["url"] == None)).all()
                    else:
                        open_suggestions = Suggestion.query.filter(and_(Suggestion.status.in_(
                        upperCaseStatusValuesList), Suggestion.suggestion_type.in_(conditionsForSuggestionTypes(filters)),\
                             Suggestion.yse_term["url"] == None)).all()
                elif inYSE == 'both':
                    if ifItIsExcluded:
                        open_suggestions = Suggestion.query.filter(and_(Suggestion.status.notin_(
                        upperCaseStatusValuesList), Suggestion.suggestion_type.in_(conditionsForSuggestionTypes(filters)))).all()
                    else:
                        open_suggestions = Suggestion.query.filter(and_(Suggestion.status.in_(
                        upperCaseStatusValuesList), Suggestion.suggestion_type.in_(conditionsForSuggestionTypes(filters)))).all()
                else:
                    print("Please, check the passed arguments")
            except Exception as ex:
                    print(str(ex))
                    return {'code': 404, 'error': str(ex)}, 404

            graph = None
            for suggestion in open_suggestions:
                graph = suggestionToGraph(suggestion.as_dict(), graph)
            try:
                # return graph.serialize(format='turtle')
                return graph.serialize(format=formatInUse(filters))
            except Exception as ex:
                print(str(ex))

        elif "suggestion_id:0" not in filters:
            tempId = filters.split("suggestion_id:", 1)[1]
            try:
                suggestion = Suggestion.query.filter_by(id=tempId).first()
                graph = suggestionToGraph(suggestion.as_dict())
                try:
                    return graph.serialize(format=formatInUse(filters))
                except Exception as ex:
                    print(str(ex))
            except Exception as ex:
                print(str(ex))
                return {'code': 404, 'error': str(ex)}, 404
        else:
            print('Please, check the passed arguments')
    else:
        return {'code': 400, 'error': str(ex)}, 400

