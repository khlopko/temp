#!flask/bin/python

from app import db
from global_keys import Key


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(32), index=True, unique=True, nullable=False)
    course = db.Column(db.Integer, index=True, nullable=False)
    lessons = db.relationship('Lesson', backref='group', lazy='dynamic')

    def __repr__(self):
        return '<Group %r>' % (self.title)

    def serialized(self):
        return {
            Key.id: self.id,
            Key.title: self.title,
        }
