# app/models.py: User database model and Evaluation model
from datetime import datetime
from .db import db

class User(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    evalutaion = db.relationship('Evaluation', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Evaluation(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    marks = db.Column(db.Integer)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Evaluation {}>'.format(self.body)

    def tojson(self):
        d = self.__dict__
        for k, v in d.items():
            if k == "_sa_instance_state":
                del d[k]
                return d



