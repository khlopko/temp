#!flask/bin/python

from app import jsonify, abort
from models import *
from models.lector import Lector
from groups import *
from lessons import *


groupsContent = GroupsContent()
lessonsContent = LessonsContent()


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
