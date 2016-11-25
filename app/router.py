#!flask/bin/python

from flask import request
from app import jsonify, abort
from models import *
from models.lector import Lector
from models.bell import Bell
from groups import *
from lessons import *
from bells import BellsContent
from errors_helper import ErrorHelper, StatusCode


groupsContent = GroupsContent()
lessonsContent = LessonsContent()
bellsContent = BellsContent()


def getBells():
    bells = map(Bell.serialized, Bell.query.all())
    json = {'bells': bells}

    return jsonify(json)


def createBell():
    if request.method != 'POST':
        abort(400)

    if request.headers['Content-Type'] != 'application/json':
        abort(400)

    json = request.get_json().copy()
    bell, code = bellsContent.add_from_json(json)

    if code is not None and code != StatusCode.ok:
        return jsonify(ErrorHelper.make_response_for_code(code))

    if bell is None:
        abort(400)

    return jsonify(bell.serialized())


def deleteBell(id):
    if request.method != 'DELETE':
        abort(400)

    code = bellsContent.delete_with_id(id)

    if code == StatusCode.ok:
        return jsonify({})
    
    return jsonify(ErrorHelper.make_response_for_code(code))
    

def getGroups():
    groups = map(Group.serialized, groupsContent.all())
    json = {'groups': groups}

    return jsonify(json)


def getLessons(groupId):
    lessons = map(Lesson.serialized, groupsContent.get(groupId).lessons)
    json = {'lessons': lessons}

    return jsonify(json)


def getLectors():
    lectors = map(Lector.serialized, Lector.query.all())
    json = {'lectors': lectors}

    return jsonify(json)


def getLector(lectorId):
    lector = Lector.query.filter(Lector.id == lectorId).first()
    
    if lector is not None:
        return jsonify(lector.serialized)
    else:
        abort(404)
