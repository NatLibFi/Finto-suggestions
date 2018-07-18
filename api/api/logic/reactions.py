import connexion
from ..models import Reaction
from .common import get_one_or_404, get_all_or_404, create_or_404, delete_or_404, update_or_404


def get_reactions(limit: int = None, offset: int = None) -> str:
    """
    Returns all reactions.

    Request query can be limited with additional parameters.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All reactions matching the query in json format
    """

    return get_all_or_404(Reaction, limit, offset)


def get_reaction(reaction_id: int) -> str:
    """
    Returns a reaction by id.

    :param reaction_id: Meeting id
    :returns: A single reaction object as json
    """

    return get_one_or_404(Reaction, reaction_id)


def post_reaction() -> str:
    """
    Creates a single reaction.
    Request body should include a single reactions object.

    :returns: the created reaction as json
    """

    return create_or_404(Reaction, connexion.request.json)


def delete_reaction(reaction_id: int) -> str:
    """
    Deletes a reaction by id.

    :param reaction_id: reaction id
    :returns: 204, No Content on success, 404 on error
    """

    return delete_or_404(Reaction, reaction_id)


def put_reaction(reaction_id: int) -> str:
    """
    Updates a single reaction by id.
    Request body should include a single reaction object.

    :returns: the created reaction as json
    """

    return update_or_404(Reaction, reaction_id, connexion.request.json)
