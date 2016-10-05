#!flask/bin/python

from app import app, jsonify, db, models, make_response, error, abort

#
# List of all groups
#


def getGroups():
    groups = map(parseGroup, models.Group.query.all())
    json = {'groups': groups}

    return jsonify(json)


def parseGroup(group):
    return {
        'id': group.id,
        'title': group.title,
    }

#
# Concrete group lessons by groupId.
#


def getLessons(groupId):
    lessons = map(parseLesson, models.Lesson.query.filter(models.Lesson.groupId == groupId).all())
    json = {'lessons': lessons}

    return jsonify(json)


def parseLesson(lesson):
    return {
        'id': lesson.id,
        'title': lesson.title,
        'room': lesson.room,
        'lector': parseLector(lesson.lector),
        'dayOfWeek': lesson.dayOfWeek,
        'weekNumber': lesson.weekNumber,
        'position': lesson.position,
    }

#
# List of all lectors.
#


def getLectors():
    lectors = map(parseLector, models.Lector.query.all())
    json = {'lectors': lectors}

    return jsonify(json)


def getLector(lectorId):
    lector = models.Lector.query.filter(models.Lector.id == lectorId).first()
    if lector is not None:
        return jsonify(parseLector(lector))
    else:
        abort(404)


def parseLector(lector):
    return {
        'id': lector.id,
        'firstname': lector.firstname,
        'lastname': lector.lastname,
        'sorname': lector.sorname,
    }
