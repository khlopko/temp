#!flask/bin/python

from app import models, db
from models.lector import Lector
from errors_helper import StatusCode


class LectorsContent:

    def __init__(self):
        self.helper = LectorsHelper()

    def create_from_json(self, json):
        lector = Lector.parse(json)
        code = self.helper.is_exists(lector)
        
        if code == StatusCode.ok:
            db.session.add(lector)
            db.session.commit()

            return (lector, code)

        return (None, code)


class LectorsHelper:

    def is_exists(self, lector):
        fetched = Lector.query.filter(
            Lector.firstname == lector.firstname, 
            Lector.sorname == lector.sorname, 
            Lector.lastname == lector.lastname).first()
        if fetched is not None:
            return StatusCode.already_exists
        else:
            return StatusCode.ok
