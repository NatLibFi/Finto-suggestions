import connexion

from ..authentication import admin_only
from ..models import Tag
from .common import get_one_or_404, get_all_or_400, create_or_400, delete_or_404, update_or_404_custom


def get_tags(limit: int = None, offset: int = None) -> str:
    """
    Returns all tags.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All tags matching the query in json format
    """

    return get_all_or_400(Tag, limit, offset)


def get_tag(tag_label: str) -> str:
    """
    Returns a tag by label.

    :param tag_label: tag label
    :returns: A single tag object as json
    """

    return get_one_or_404(Tag, tag_label.upper())


@admin_only
def post_tag() -> str:
    """
    Creates a single tag.
    Request body should include a single tag object.

    :returns: the created tag as json
    """

    return create_or_400(Tag, connexion.request.json)


@admin_only
def put_tag(tag_label: str) -> str:
    """
    Updates a single tag by label.
    Request body should include a single tag object.

    :param tag_label: tag label
    :returns: the created tag as json
    """

    return update_or_404_custom(Tag, tag_label, connexion.request.json)


@admin_only
def delete_tag(tag_label: str) -> str:
    """
    Deletes a tag by label.

    :param tag_label: tag label
    :returns: 204, No Content on success, 404 on error
    """

    return delete_or_404(Tag, tag_label.upper())
