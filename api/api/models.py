from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import validates
from passlib.hash import pbkdf2_sha256 as hash_algorithm
from datetime import datetime
from collections import Counter
import enum

db = SQLAlchemy()

suggestions_to_tags = db.Table('suggestion_tags_association',
                               db.Column('tag_label', db.String, db.ForeignKey(
                                   'tags.label'), primary_key=True),
                               db.Column('suggestion_id', db.Integer, db.ForeignKey(
                                   'suggestions.id'), primary_key=True)
                               )


class EventTypes(enum.IntEnum):
    ACTION = 0
    COMMENT = 1


class SuggestionStatusTypes(enum.IntEnum):
    DEFAULT = 0
    REJECTED = 1
    ACCEPTED = 2


class SuggestionTypes(enum.IntEnum):
    NEW = 0
    MODIFY = 1


class UserRoles(enum.IntEnum):
    NORMAL = 0
    ADMIN = 1


class SerializableMixin():
    """
    Adds the method ´as_dict´ to an sqlalchemy model.

    Calling the method requires a special __public__ attribute,
    which acts as a whitelist for serializable columns.

    e.g. __public__ = ['id', 'created', 'modified']
    """

    def _serialize(self, obj):
        """
        A simple serializer override to handle Enums better.
        This could also be done on overriding flask_app.json_encoder.
        """
        if isinstance(obj, enum.Enum):
            return obj.name
        return obj

    def as_dict(self, strip=True):
        d = {c.name: self._serialize(getattr(self, c.name))
             for c in self.__table__.columns}
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
                  'reactions', 'user_id', 'suggestion_id', 'created', 'modified']

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    event_type = db.Column(db.Enum(EventTypes), nullable=False)
    text = db.Column(db.Text)

    reactions = db.relationship('Reaction', backref='event')

    # user: backref
    # suggestion: backref

    suggestion_id = db.Column(db.Integer, db.ForeignKey('suggestions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        msg = self.text if len(self.text) <= 16 else (self.text[:16] + '...')
        return '<Event {} | \'{}\'>'.format(self.event_type.name, msg)

    def as_dict(self, strip=True):
        serialized = super(Event, self).as_dict()
        serialized['reactions'] = [e.as_dict() for e in self.reactions]
        return serialized


class Reaction(db.Model, SerializableMixin):
    __tablename__ = 'reactions'
    __public__ = ['id', 'code', 'event_id', 'suggestion_id', 'user_id']

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


class Meeting(db.Model, SerializableMixin):
    __tablename__ = 'meetings'
    __public__ = ['id', 'name', 'created', 'modified', 'meeting_date']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    meeting_date = db.Column(db.DateTime, index=True)

    suggestions = db.relationship(
        'Suggestion', backref='meeting')

    def __repr__(self):
        return '<Meeting {}>'.format(self.id)

    def as_dict(self, strip=True):
        serialized = super(Meeting, self).as_dict()
        serialized['suggestions'] = [
            e.id for e in self.suggestions]  # only ids

        serialized['processed'] = Counter(
            [s.status.name.upper() for s in self.suggestions])

        return serialized


class Suggestion(db.Model, SerializableMixin):
    __tablename__ = 'suggestions'
    __public__ = ["alternative_label", "broader", "created", "description", "group", "id", "created", "modified",
                  "narrower", "organization", "preferred_label", "reason", "related", "status", "suggestion_type", "uri", "meeting_id"]

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    modified = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # meeting: backref

    # suggestion_type = db.Column(db.Enum(SuggestionTypes), nullable=False)
    suggestion_type = db.Column(db.Enum(SuggestionTypes))
    status = db.Column(db.Enum(SuggestionStatusTypes),
                       default=SuggestionStatusTypes.DEFAULT)
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
    reactions = db.relationship('Reaction', backref='suggestion')

    tags = db.relationship("Tag",
                           secondary=suggestions_to_tags,
                           backref="suggestions")

    meeting_id = db.Column(db.Integer, db.ForeignKey('meetings.id'))

    def __repr__(self):
        label = self.preferred_label.get('fi')
        return '<Suggestion \'{}\'>'.format(label)

    def as_dict(self, strip=True):
        # relationships (joins) should be expanded carefully
        serialized = super(Suggestion, self).as_dict()
        serialized['events'] = [e.id for e in self.events]  # only ids
        serialized['reactions'] = [
            e.as_dict(strip=strip) for e in self.reactions]
        serialized['tags'] = [e.as_dict(strip=strip) for e in self.tags]
        return serialized


class Tag(db.Model, SerializableMixin):
    __tablename__ = "tags"
    __public__ = ['label']

    label = db.Column(db.String(128), index=True, primary_key=True)
    # suggestions: backref

    # convert tag always to uppercase
    @validates('label')
    def convert_upper(self, key, value):
        return value.upper()

    def __repr__(self):
        return '<Tag {}>'.format(self.label)

    def as_dict(self, strip=True):
        serialized = super(Tag, self).as_dict()
        serialized['suggestions'] = [
            e.id for e in self.suggestions]  # only ids
        return serialized


class User(db.Model, SerializableMixin):
    __tablename__ = 'users'
    __public__ = ['id', 'name', 'email', 'role']

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(64), index=True, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    role = db.Column(db.Enum(UserRoles), default=UserRoles.NORMAL)
    password_hash = db.Column(db.String(128))

    events = db.relationship('Event', backref='user')

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value):
        self.password_hash = hash_algorithm.hash(value)

    def validate_password(self, password):
        return hash_algorithm.verify(password, self.password_hash)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def as_dict(self, strip=True):
        # relationships (joins) should be expanded carefully
        serialized = super(User, self).as_dict()
        # serialized['events'] = [e.as_dict(strip=strip) for e in self.events]  # whole events
        serialized['events'] = [e.id for e in self.events]  # only ids
        return serialized


class TokenBlacklist(db.Model, SerializableMixin):
    """
    JSON Web Token blacklist for logouts and user bans.
    """

    __tablename__ = 'tokens_blacklist'
    __public__ = ['id', 'jti', 'token_type', 'revoked', 'expires']  # as_dict

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)