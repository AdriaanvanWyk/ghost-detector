from app import db, login
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, gen_salt, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Ghost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('ghost_type.id'))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    caught = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return '<Ghost {}>'.format(self.id)


class GhostType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<GhostType {}>'.format(self.name)


class GhostCode(db.Model):
    code = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<GhostCode {}>'.format(self.code)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
