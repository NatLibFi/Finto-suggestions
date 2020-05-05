# -*- coding: utf-8 -*-
import os
import smtplib
import codecs
import json
from email.mime.text import MIMEText
from datetime import datetime
from typing import Dict

from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError

from ..models import db
from ..authentication import verify_user_access_to_resource

# from sqlalchemy import create_engine  
from sqlalchemy import Table, Column, String, MetaData



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


def id_exists(model: object, object_id: int) -> bool:
    """
    Checks if the given id exists in the given model object.

    :param object_id: id to search
    :param model: model to search from
    :returns: True if id exists, or id is None. False if user was not found in the model.
    """

    if object_id is None:
        return False

    return db.session.query(exists().where(model.id == object_id)).scalar()


def get_all_or_400_custom(query) -> str:
    """
        A generic get all, with a custom query function

        :param query: query instance
        :returns: All columns matching the query or 400
    """
    try:
        db_objs = query.all()
    except InvalidFilterException as e:
        return create_response({}, 400, str(e))

    serialized_objects = []
    if db_objs:
        serialized_objects = [o.as_dict() for o in db_objs]

    return create_response(serialized_objects, 200)


def get_all_or_400(model: object, limit: int, offset: int) -> str:
    """
    Returns all queried objects.
    Request query can be limited with additional parameters `limit` and `offset`.

    :param limit: Cap the results to :limit: results
    :param offset: Start the query from offset (e.g. for paging)
    :returns: All columns matching the query in json format or 400 and error message as JSON
    """

    query = model.query
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)

    return get_all_or_400_custom(query)

def get_selected_or_400(model: object):
    """
    Todo: Must be fixed to read selected entities as an argument.

    Returns all queried objects.

    :returns: All columns matching the query or 400 and error message
    """
 
    db_selected_objs = model.query.with_entities(model.id, model.name, model.created, model.modified, model.meeting_date)
    serialized_objects = []
    if db_selected_objs:
        serialized_objects = [o for o in db_selected_objs]
    
    error_msg = "Did not find any data"

    if db_selected_objs:
        return create_response(serialized_objects, 200)

    return create_response(None, 404, error_msg)
    

def get_one_or_404(model: object, primary_key: int) -> str:
    """
    Returns an object by primary_key.

    :param meeting_id: database column id
    :returns: success 200 with a serialized object or 404 and an error message as JSON
    """
    db_obj = model.query.get(primary_key)

    if db_obj:
        return create_response(db_obj.as_dict(), 200)

    msg = "Unable to find any {} with an id of {}.".format(
        model.__table__, primary_key)
    return create_response(None, 404, msg)


def get_count_or_400_custom(query) -> str:
    """
        Runs function count() on given query.

        :param query: query instance
        :returns: Row count of query or 400
    """
    try:
        db_count = query.count()
    except InvalidFilterException as e:
        return create_response(0, 400, str(e))

    return create_response({"count": db_count}, 200)


def create_or_400(model: object, payload: Dict, error_msg: str = None) -> str:
    """
    Creates a new object and commits it to the database.
    Checks if there is a need to send email. The sending depends always on Model
    :param model: database model to create
    :param payload: a single object
    :returns: the created user as json
    """
    db_obj = model(**payload)

    verify_user_access_to_resource(db_obj)

    try:
        db.session.add(db_obj)
        db.session.commit()
    except IntegrityError:
        msg = "Unable to create a new {}".format(str(model.__table__)[:-1])
        if error_msg:
            msg = error_msg
        db.session.rollback()
        return create_response(None, 400, msg)

    try:
        if db_obj.email:
            send_email_while_signing_up(db_obj.email)
    except Exception as exx:
        print("The object has no attribute --> " + str(exx))

    return create_response(db_obj.as_dict(), 201)


def delete_or_404(model: object, primary_key: int) -> str:
    """
    Deletes an object by primary_key from the database.

    :param model: sqlalchemy database object (column) to delete from
    :param primary_key: primary_key
    :returns: 204, No Content on success, 404 on error
    """

    db_obj = model.query.get(primary_key)

    if not db_obj:
        msg = "No {} found with id {}.".format(model.__table__, primary_key)
        return create_response(None, 404, msg)

    verify_user_access_to_resource(db_obj)

    db.session.delete(db_obj)
    db.session.commit()
    return (None, 204)  # No Content


def update_or_404(model: object, primary_key: int, payload: Dict) -> str:
    """
    Updates a single sqlalchemy model by id.

    :param model: SQLAlchemy database model
    :param primary_key: updated primary_key
    :param payload: payload to update the object with
    :returns: the updated object as json, or 404
    """

    old_object = model.query.get(primary_key)
    if not old_object:
        msg = "{} with an id {} doesn't exist.".format(
            str(model.__table__)[:-1], primary_key)
        return create_response(None, 404, msg)

    verify_user_access_to_resource(old_object)

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


def update_or_404_custom(model: object, primary_key: int, payload: Dict) -> str:
    """
    Updates a single sqlalchemy model by label.

    :param model: SQLAlchemy database model
    :param primary_key: updated primary_key
    :param payload: payload to update the object with
    :returns: the updated object as json, or 404
    """

    old_object = model.query.get(primary_key)
    if not old_object:
        msg = "{} with an id {} doesn't exist.".format(
            str(model.__table__)[:-1], primary_key)
        return create_response(None, 404, msg)

    # create a new model instance, but replace its id
    db_obj = model(**payload)
    db_obj.label = old_object.label

    db.session.merge(db_obj)
    db.session.commit()

    return create_response(db_obj.as_dict(), 200)


def patch_or_404(model: object, primary_key: int, payload: Dict) -> str:
    """
    Patches a single sqlalchemy model by primary_key.

    :param model: SQLAlchemy database model
    :param primary_key: patched objects primary_key
    :param payload: payload to patch the object with
    :returns: the patched object as json, or 404
    """

    db_obj = model.query.get(primary_key)
    if not db_obj:
        msg = "{} with an id {} doesn't exist.".format(
            str(model.__table__)[:-1], primary_key)
        return create_response(None, 404, msg)

    verify_user_access_to_resource(db_obj)

    # make sure that the `id` and `created` fields never get updated
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


def send_email_while_signing_up(email: str) -> str:
    """
    Method for sending email messages
    """

    if email:
        email_server_address = os.environ.get('EMAIL_SERVER_ADDRESS')
        email_server_port = os.environ.get('EMAIL_SERVER_PORT')
        default_sender = os.environ.get('EMAIL_SERVER_DEFAULT_SENDER_EMAIL')
        email_server_username = os.environ.get('EMAIL_SERVER_USERNAME')
        email_server_password = os.environ.get('EMAIL_SERVER_PASSWORD')

        body_string_raw = os.environ.get('WELCOME_MESSAGE_BODY')
        subject_string_raw = os.environ.get('WELCOME_SUBJECT') 
        body = MIMEText(body_string_raw.encode("utf-8"), _charset='utf-8')
        subject_text = MIMEText(subject_string_raw.encode("utf-8"), _charset='utf-8')

        # body = body_string_raw.encode('ascii','ignore')
        # subject_text = subject_string_raw.encode('ascii','ignore')


        message = 'Subject: {}\n\n{}'.format(
            subject_text,
            body)

        try:
            mailserver = smtplib.SMTP(email_server_address, email_server_port)
            mailserver.ehlo()
            mailserver.starttls()

            if email_server_username and email_server_password:
                mailserver.login(email_server_username, email_server_password)

            mailserver.sendmail(default_sender, [email], message)
            mailserver.quit()
            return True
        except Exception as ex:
            print(str(ex))
    return False
