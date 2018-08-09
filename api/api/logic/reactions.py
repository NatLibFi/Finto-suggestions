import connexion
from ..authentication import authorized
from .validators import reaction_parameter_validator
from ..models import Reaction
from .common import (get_one_or_404, get_all_or_404, create_or_404,
                     delete_or_404, update_or_404, patch_or_404)


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


@authorized
@reaction_parameter_validator
def post_reaction() -> str:
    """
    Creates a single reaction.
    Request body should include a single reactions object.

    :returns: the created reaction as json
    """

    return create_or_404(Reaction, connexion.request.json)


@authorized
def delete_reaction(reaction_id: int) -> str:
    """
    Deletes a reaction by id.

    :param reaction_id: reaction id
    :returns: 204, No Content on success, 404 on error
    """

    return delete_or_404(Reaction, reaction_id)


@authorized
@reaction_parameter_validator
def put_reaction(reaction_id: int) -> str:
    """
    Updates a single reaction by id.
    Request body should include a single reaction object.

    :returns: the created reaction as json
    """

    return update_or_404(Reaction, reaction_id, connexion.request.json)


@authorized
@reaction_parameter_validator
def patch_reaction(reaction_id: int) -> str:
    """
    Patches a single reaction by id.
    Request body should include a single (partial) reaction object.

    :returns: the patched reaction as json
    """

    return patch_or_404(Reaction, reaction_id, connexion.request.json)
