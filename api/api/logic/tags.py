import connexion
from ..models import db, Tag
from .common import create_response, id_exists, get_one_or_404, get_all_or_404, create_or_404, delete_or_404, update_or_404


def get_tags(limit: int = None, offset: int = None) -> str:
    """
    Returns all tags.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All tags matching the query in json format
    """

    return get_all_or_404(Tag, limit, offset)


def get_tag(tag_id: int) -> str:
    """
    Returns a tag by id.

    :param tag_id: tag id
    :returns: A single tag object as json
    """

    return get_one_or_404(Tag, tag_id)


def post_tag() -> str:
    """
    Creates a single tag.
    Request body should include a single tag object.

    :returns: the created tag as json
    """

    return create_or_404(Tag, connexion.request.json)


def delete_tag(tag_id: int) -> str:
    """
    Deletes a tag by id.

    :param tag_id: tag id
    :returns: 204, No Content on success, 404 on error
    """

    return delete_or_404(Tag, tag_id)


def put_tag(tag_id: int) -> str:
    """
    Updates a single tag by id.
    Request body should include a single tag object.

    :returns: the created tag as json
    """

    return update_or_404(Tag, tag_id, connexion.request.json)
