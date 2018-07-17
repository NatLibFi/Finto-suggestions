from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
import enum

db = SQLAlchemy()

suggestions_to_tags = db.Table('suggestion_tags_association',
                               db.Column('tag_id', db.Integer, db.ForeignKey(
                                   'tags.id'), primary_key=True),
                               db.Column('suggestion_id', db.Integer, db.ForeignKey(
                                   'suggestions.id'), primary_key=True)
                               )


# TODO: 0 and 1
class EventTypes(enum.IntEnum):
    ACTION = 1
    COMMENT = 2


class SuggestionStatusTypes(enum.IntEnum):
    DEFAULT = 0
    REJECTED = 1
    ACCEPTED = 2


class SuggestionTypes(enum.IntEnum):
    NEW = 0
    MODIFY = 1


class SerializableMixin():
    """
    Adds the method ´as_dict´ to an sqlalchemy model.

    Calling the method requires a special __public__ attribute,
    which acts as a whitelist for serializable columns.

    e.g. __public__ = ['id', 'created', 'modified']
    """

    def as_dict(self, strip=True):
        d = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        if strip:  # strip hidden fields, such as meeting_id
            d = {k: v for k, v in d.items() if k in self.__public__}
        return d


class Event(db.Model, SerializableMixin):
    """
    An object representing a single event in a suggestion's event stream.
    It can be an action, or a comment by a user, for example.
    """

    __tablename__ = 'events'
    __public__ = ['id', 'event_type', 'text',
                  'emojis', 'user_id', 'suggestion_id']

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    event_type = db.Column(db.Enum(EventTypes), nullable=False)
    text = db.Column(db.Text)

    emojis = db.relationship('Emoji', backref='event')

    # user: backref
    # suggestion: backref

    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        msg = self.text if len(self.text) <= 16 else (self.text[:16] + '...')
        return '<Event {} | \'{}\'>'.format(self.event_type.name, msg)


class Emoji(db.Model):
    __tablename__ = 'emojis'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", backref=db.backref("user", uselist=False))

    # suggestion: backref
    # event: backref

    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestions.id'))

    def __repr__(self):
        return '<Emoji {}>'.format(self.code)


class Meeting(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    suggestions = db.relationship(
        'Suggestion', backref='meeting')

    def __repr__(self):
        return '<Meeting {}>'.format(self.id)


class Suggestion(db.Model, SerializableMixin):
    __tablename__ = 'suggestions'
    __public__ = ["alternative_label", "broader", "created", "description", "group", "id", "created", "modified",
                  "narrower", "organization", "preferred_label", "reason", "related", "status", "suggestion_type", "uri"]

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # meeting: backref

    # suggestion_type = db.Column(db.Enum(SuggestionTypes), nullable=False)
    suggestion_type = db.Column(db.Enum(SuggestionTypes))
    status = db.Column(db.Enum(SuggestionStatusTypes))
    uri = db.Column(db.String(256))

    organization = db.Column(db.String(256))
    description = db.Column(db.Text)
    reason = db.Column(db.Text)

    preferred_label = db.Column(db.JSON)
    alternative_label = db.Column(db.JSON)

    broader = db.Column(db.JSON)
    narrower = db.Column(db.JSON)
    related = db.Column(db.JSON)
    group = db.Column(db.JSON)

    events = db.relationship('Event', backref='suggestion')
    emojis = db.relationship('Emoji', backref='suggestion')

    tags = db.relationship("Tag",
                           secondary=suggestions_to_tags,
                           backref="suggestions")

    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'))

    def __repr__(self):
        label = self.preferred_label.get('fi')
        return '<Suggestion \'{}\'>'.format(label)


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), index=True, nullable=False)
    # suggestions: backref

    def __repr__(self):
        return '<Tag {}>'.format(self.text)


class User(db.Model, SerializableMixin):
    __tablename__ = 'users'
    __public__ = ['id', 'name', 'email']

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    events = db.relationship('Event', backref='user', lazy='dynamic')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<User {}>'.format(self.name)
