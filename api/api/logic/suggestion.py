import connexion

DUMMY_SUGGESTION = {'id': 1000,
                    'uri': 'http://www.google.fi',
                    'prefLabel': ['Kissa @fi', 'Katt @sv', 'Cat @en'],
                    'type': 0,
                    'status': 3
                    }


def get_suggestions(limit: int = None, offset: int = None) -> str:
    return {
        "data": [
            DUMMY_SUGGESTION,
            DUMMY_SUGGESTION
        ]
    }, 200


def post_suggestion() -> str:
    body = connexion.request.json
    return {
        "data": body
    }, 201


def get_suggestion(suggestion_id: int) -> str:
    return {
        "data": DUMMY_SUGGESTION
    }, 200
    # return "failed", 404


def put_suggestion(suggestion_id: int) -> str:
    body = connexion.request.json
    return {
        "data": body
    }, 204
    # 404


def patch_suggestion(suggestion_id: int) -> str:
    body = connexion.request.json
    patched = DUMMY_SUGGESTION.copy()
    patched.update(body)

    return {
        "data": patched
    }, 200
    # return "patch failed", 404


def delete_suggestion(suggestion_id: int) -> str:
    return {
        "data": DUMMY_SUGGESTION
    }, 204
    # return "delete failed", 404
