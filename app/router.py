#!flask/bin/python

from app import app, jsonify, db, models, make_response, error, abort

defaultPath = '/api/v0.1/'

#
# List of all groups
#

@app.route(defaultPath + 'groups', methods=['GET'])
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

@app.route(defaultPath + 'groups/<int:groupId>/lessons', methods=['GET'])
def getGroup(groupId):
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

@app.route(defaultPath + 'lectors', methods=['GET'])
def getLectors():
    lectors = map(parseLector, models.Lector.query.all())
    json = {'lectors': lectors}

    return jsonify(json)

@app.route(defaultPath + 'lectors/<int:lectorId>', methods=['GET'])
def getLector(lectorId):
    lector = models.Lector.query.filter(models.Lector.id == lectorId).first()
    if lector != None:
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
