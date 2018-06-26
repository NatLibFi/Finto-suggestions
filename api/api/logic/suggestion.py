

def get_suggestions(limit: int = None, offset: int = None) -> str:
    return [
        {'id': 1000,
         'uri': 'http://www.google.fi',
         'prefLabel': ['Kissa @fi', 'Katt @sv', 'Cat @en'],
         'type': 0,
         'status': 3
         }
    ], 200


def post_suggestion() -> str:
    return "success!", 201
    # TODO: failed status code missing


def get_suggestion(suggestion_id: int) -> str:
    return "success get", 200
    # return "failed", 404


def put_suggestion(suggestion_id: int) -> str:
    return "success put", 200
    # return "failed", 404


def patch_suggestion(suggestion_id: int) -> str:
    # TODO: requires a schema for object body
    return "success patch", 200
    # return "patch failed", 404


def delete_suggestion(suggestion_id: int) -> str:
    return "success delete", 204
    # return "delete failed", 404
