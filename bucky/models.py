from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
)
from flask import current_app
from . import db
from bucky.exceptions import ValidationError


class User(db.Model):
    """ User Database Model """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        """
        Prevents access to password property,
        ensuring it can't be read.
        """
        raise AttributeError("password is not a readable attribute.")

    @password.setter
    def password(self, password):
        """
        Sets password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Verificiation of password.
        Checks if password matches.
        """
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=20000):
        """
        Generating an authentication token that expires in 20 minutes
        """
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            """When token is valid but expired """
            return None
        except BadSignature:
            """When token is invalid """
            return None
        user = User.query.get(data["id"])
        return user


class BucketList(db.Model):
    """ Bucketlist Database Model  """

    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now,
                              onupdate=datetime.now)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"),
                           nullable=True)

    items = db.relationship("Item",
                            backref=db.backref("bucketlist"), lazy='dynamic')

    def __repr__(self):
        return "<Bucketlist: %r>" % self.title

    def to_json(self):
        """Serializes Bucketlist details into JSON"""
        json_bucketlist = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'items': [item.to_json() for item in self.items],
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'created_by': self.created_by
        }
        return json_bucketlist

    @staticmethod
    def from_json(json_bucketlist):
        title = json_bucketlist.get('title')
        description = json_bucketlist.get('description')
        if title is None or title == '':  # A bucketlist should have a title
            raise ValidationError('Bucketlist does not have a title.')
        if description is None:
            raise ValidationError('Description not found.')
        return BucketList(title=title, description=description)


class Item(db.Model):
    """ Item Database Model """

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    description = db.Column(db.Text)
    status = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime,
                              onupdate=datetime.now)

    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlists.id"))

    def __repr__(self):
        return "<Bucketlist Item: %r>" % self.title

    def to_json(self):
        """Serializes Bucketlist Items details into JSON"""
        json_item = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
        }
        return json_item

    @staticmethod
    def from_json(json_item):
        title = json_item.get('title')
        description = json_item.get('description')
        status = json_item.get('status')
        if title is None or title == '':  # A bucketlist should have a title
            raise ValidationError('Item does not have a title.')
        if description is None:
            raise ValidationError('Description not found.')
        return Item(title=title, description=description, status=status)
