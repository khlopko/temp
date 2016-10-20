#!flask/bin/python

from app import db
from global_keys import Key


class Lector(db.Model):
    __tablename__ = 'lectors'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(64), index=True, nullable=False)
    sorname = db.Column(db.String(64), index=True, nullable=False)
    lastname = db.Column(db.String(64), index=True, nullable=False)
    lessons = db.relationship('Lesson', backref='lector', lazy='dynamic')

    def __repr__(self):
        return '<Lector %r>' % (self.firstname)

    def serialized(self):
        return {
            Key.id: self.id,
            Key.firstname: self.firstname,
            Key.lastname: self.lastname,
            Key.sorname: self.sorname,
        }
