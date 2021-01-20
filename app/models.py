from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin

from app import db, bcrypt


class User(db.Model, UserMixin):

    ''' A user who has an account on the website. '''

    __tablename__ = 'users'

    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    confirmation = db.Column(db.Boolean)
    paid = db.Column(db.Boolean)
    _password = db.Column(db.String)

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def get_id(self):
        return self.email

    def is_paid(self):
        return self.paid


class TmpFriend(db.Model):

    ''' A friend added by a user who hasn't signed up. '''

    __tablename__ = 'tmp_friends'

    name = db.Column(db.String, primary_key=True)

    def get_name(self):
        return self.name


class Friend(db.Model):

    ''' A friend added by a user who has signed up. '''

    __tablename__ = 'friends'

    email = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, primary_key=True)

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name
