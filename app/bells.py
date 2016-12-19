#!flask/bin/python

from app import db
from models.global_keys import Key
from models.bell import Bell
from errors_helper import StatusCode


class BellsContent:

    def __init__(self):
        self.helper = BellsHelper()


    def all(self):
        return Bells.query.all()


    def add_from_json(self, json):
        pair_begin = json[Key.pair_begin]
        pair_end = json[Key.pair_end]
        
        if pair_begin is None or pair_end is None:
            return (None, None)

        bell = Bell(pair_begin=pair_begin, pair_end=pair_end)

        if not self.helper.is_valid(bell):
            return (None, StatusCode.already_exists)

        db.session.add(bell)
        db.session.commit()
        
        return (bell, StatusCode.ok)


    def delete_with_id(self, id):
        bell = Bell.query.filter(Bell.id == id)

        if bell is None:
            return StatusCode.not_found

        bell.delete()
        db.session.commit()
        return StatusCode.ok


class BellsHelper:

    def is_valid(self, bell):
        bell = Bell.query.filter(Bell.pair_begin == bell.pair_begin).first()
        return bell is None
