#!flask/bin/python

from flask import request
from app import jsonify, abort
from models import *
from models.lector import Lector
from models.bell import Bell
from groups import *
from lessons import *
from bells import BellsContent
from lectors import LectorsContent
from errors_helper import ErrorHelper, StatusCode


groupsContent = GroupsContent()
lessonsContent = LessonsContent()
bellsContent = BellsContent()
lectorsContent = LectorsContent()


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


def getLessons(group_id):
    lessons = map(Lesson.serialized, groupsContent.get(group_id).lessons)
    json = {'lessons': lessons}

    return jsonify(json)


def createLesson(group_id):
    json = {}
    if request.headers['Content-Type'] == 'application/json':
        json = request.get_json().copy()
    else:
        abort(400)
    json['group_id'] = group_id
    lesson, code = lessonsContent.create_from_json(json)
    if lesson is None:
        return jsonify(ErrorHelper.make_response_for_code(code))
    else:
        return jsonify(lesson.serialized)


def deleteLesson(lesson_id):
    code = lessonsContent.delete(lesson_id)
    return jsonify({})


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


def createLector():
    json = {}
    if request.headers['Content-Type'] == 'application/json':
        json = request.get_json().copy()
    else:
        abort(400)
    lector, code = lectorsContent.create_from_json(json)
    print(lector, code)
    if lector is None:
        return jsonify(ErrorHelper.make_response_for_code(code))
    else:
        return jsonify(lector.serialized)
