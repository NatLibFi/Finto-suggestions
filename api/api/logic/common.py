from datetime import datetime
from typing import Dict
from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError
from ..models import db


class InvalidFilterException(Exception):
    pass


def create_response(data: Dict, status_code: int, message: str = None, **kwargs) -> Dict:
    response_dict = {}
    data = data if data else {}

    if kwargs:
        response_dict.update(kwargs)
    if message:
        response_dict["message"] = message

    response_dict["code"] = status_code
    response_dict["data"] = data

    if isinstance(data, list):
        response_dict["items"] = len(data)

    return response_dict, status_code


def id_exists(model: object, id: int) -> bool:
    """
    Checks if the given id exists in the given model object.

    :param id: id to search
    :param model: model to search from
    :returns: True if id exists, or id is None. False if user was not found in the model.
    """

    if id and not db.session.query(exists().where(model.id == id)).scalar():
        return False
    return True


def get_all_or_404_custom(query_func) -> str:
    """
        A generic get all, with a custom query function

        :param model: model to query
        :param query_func: a function, that takes a query
            instance as a parameter and returns a query instance.

            This is handy for filtering, sorting and searching. 

            def query_func():
                query = model.query
                if limit:
                    query = query.limit(limit)
                return query.all()

        :returns: All columns matching the filtered query or 404
    """
    try:
        db_objs = query_func()
    except InvalidFilterException as e:
        return create_response({}, 404, str(e))

    serialized_objects = []
    if db_objs:
        serialized_objects = [o.as_dict() for o in db_objs]

    return create_response(serialized_objects, 200)


def get_all_or_404(model, limit: int, offset: int) -> str:
    """
    Returns all queried objects.
    Request query can be limited with additional parameters `limit` and `offset`.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All columns matching the query in json format or 404 and error message as JSON
    """

    def query_func():
        query = model.query
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)

        return query.all()

    return get_all_or_404_custom(query_func)


def get_one_or_404(model: object, object_id: int) -> str:
    """
    Returns an object by id.

    :param meeting_id: database column id
    :returns: success 200 with a serialized object or 404 and an error message as JSON
    """
    db_obj = model.query.get(object_id)

    if db_obj:
        return create_response(db_obj.as_dict(), 200)

    msg = "Could not find a {} with an id {}.".format(
        model.__table__, object_id)
    return create_response(None, 404, msg)


def create_or_404(model: object, payload: Dict, error_msg: str = None) -> str:
    """
    Creates a new object and commits it to the database.

    :param model: database model to create
    :param payload: a single object
    :returns: the created user as json
    """
    db_obj = model(**payload)

    try:
        db.session.add(db_obj)
        db.session.commit()
    except IntegrityError:
        msg = "Unable to create a new {}".format(str(model.__table__)[:-1])
        if error_msg:
            msg = error_msg
        return create_response(None, 404, msg)

    return create_response(db_obj.as_dict(), 200)


def delete_or_404(model: object, object_id: int) -> str:
    """
    Deletes an object by id from the database.

    :param model: sqlalchemy database object (column) to delete from 
    :param object_id: object id
    :returns: 204, No Content on success, 404 on error
    """

    success = model.query.filter_by(id=object_id).delete()
    db.session.commit()

    if success:
        return (None, 204)  # No Content

    msg = "No {} found with id {}.".format(
        model.__table__, object_id)
    return create_response(None, 404, msg)


def update_or_404(model: object, object_id: int, payload: Dict) -> str:
    """
    Updates a single sqlalchemy model by id.

    :param model: SQLAlchemy database model
    :param object_id: updated objects id
    :param payload: payload to update the object with
    :returns: the updated object as json, or 404
    """

    old_object = model.query.get(object_id)
    if not old_object:
        msg = "{} with an id {} doesn't exist.".format(
            model.__table__, object_id)
        return create_response(None, 404, msg)

    # create a new model instance, but replace its id
    db_obj = model(**payload)
    db_obj.id = old_object.id
    if 'modified' in model.__table__.columns:
        db_obj.modified = datetime.utcnow()
    if 'created' in model.__table__.columns:
        db_obj.created = old_object.created

    db.session.merge(db_obj)
    db.session.commit()

    return create_response(db_obj.as_dict(), 200)


def patch_or_404(model: object, object_id: int, payload: Dict) -> str:
    """
    Patches a single sqlalchemy model by id.

    :param model: SQLAlchemy database model
    :param object_id: patched objects id
    :param payload: payload to patch the object with
    :returns: the patched object as json, or 404
    """

    db_obj = model.query.get(object_id)
    if not db_obj:
        msg = "{} with an id {} doesn't exist.".format(
            model.__table__, object_id)
        return create_response(None, 404, msg)

    # make sure that the id and created fields never get updated
    payload.pop("id", None)
    payload.pop("created", None)

    # update SQLAlchemy object with new attributes
    for key, value in payload.items():
        setattr(db_obj, key, value)

    # update the modified field, also
    if 'modified' in model.__table__.columns:
        db_obj.modified = datetime.utcnow()

    try:
        db.session.commit()
    except IntegrityError:
        msg = "Unable to patch the {}. Please check that all properties have valid values.".format(
            str(model.__table__)[:-1])
        return create_response(None, 404, msg)

    return create_response(db_obj.as_dict(), 200)
