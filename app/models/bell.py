#!flask/bin/python

from app import db
from global_keys import Key


class Bell(db.Model):
    __tablename__ = 'bells'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pair_begin = db.Column(db.String(8), index=True, nullable=False)
    pair_end = db.Column(db.String(8), index=True, nullable=False)

    def __repr__(self):
        return '<Lector %r %r>' % (self.pair_begin, self.pair_end)

    def serialized(self):
        return {
            Key.id: self.id,
            Key.pair_begin: self.pair_begin,
            Key.pair_end: self.pair_end,
        }