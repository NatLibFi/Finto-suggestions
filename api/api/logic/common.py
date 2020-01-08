import os
import smtplib
from datetime import datetime
from typing import Dict

from sqlalchemy import exists
from sqlalchemy.exc import IntegrityError

from ..models import db
from ..authentication import verify_user_access_to_resource


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


def get_all_or_404_custom(query_func) -> str:
    """
        A generic get all, with a custom query function

        :param model: model to query
        :param query_func: a function, that takes a query
            instance as a parameter and returns a query instance.

            This is handy for filtering, sorting and searching.

            def query_func()
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


def get_count_or_404_custom(query_func) -> str:
    """
        Gets count of objects, with a custom query function

        :param model: model to query
        :param query_func: a function, that takes a query
            instance as a parameter and returns a query instance.

            This is handy for filtering, sorting and searching.

            def query_func()
                query = model.query
                if limit:
                    query = query.limit(limit)
                return query.all()

        :returns: All columns matching the filtered query or 404
    """
    try:
        db_count = query_func()
    except InvalidFilterException as e:
        return create_response(0, 404, str(e))

    return create_response({"count": db_count}, 200)


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
# Mika's testing begins

    try:
        print("*** If User Object has an email it is used to send a Welcome email ***")
        # if db_obj.attributes:
        #     print(db_obj.attributes)
        #     if 'email' in db_obj.attributes:
        if db_obj.email:
            print("The email in use is " + db_obj.email)
            send_email_while_signing_up(db_obj.email)
    except Exception as exx:
        print("The object has no attribute --> " + str(exx))


    # if db_obj.attributes:

    #     if db_obj.
    #     if 'User' in db_obj.attributes:
    #         print("ja kaikki sanoo moooooi")
    #     else:
    #         print(db_obj.attributes)

#Tarvitaan, mutta korjaa
    # if db_obj.email:
    #     print("***********************")
    #     print("***********************")
    #     print("***********************")
    #     print("***********************")
    #     print(model.__str__())
    #     print("The email in use is " + db_obj.email )
    #     send_email_while_signing_up(db_obj.email)

        # if password_update_success is True:
        #   sending_status = send_email(new_password, user.email)
        #   if sending_status:
        #     return { 'code': 200 }, 200
        #   else:
        #     return { 'code': 404, 'error': 'Could not send email' }, 404

# Mika's testing ends
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

        body = os.environ.get('WELCOME_MESSAGE_BODY')
        subject_text = os.environ.get('WELCOME_SUBJECT')

# WELCOME_SUBJECT='Tervetuloa systeemiin'
# WELCOME_MESSAGE_BODY="""Mikan testiteksti"""


        print(email_server_address)
        print(email_server_port)
        print(default_sender)
        print(email_server_username)

# Toimiva
    #   body = """
    #   Mikan testiteksti
    #   """

    #   message = 'Subject: Tervetuloa Ehdotusjärjestelmän käyttäjäksi'.format(body)


        message = 'Subject: {}\n\n{}'.format(
            # TOIMIVA 'Tervetuloa systeemiin',
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
