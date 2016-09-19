#!flask/bin/python

from app import app, jsonify, db, models, make_response, error, abort

defaultPath = '/api/v0.1/'

#
# List of all groups
#

@app.route(defaultPath + 'groups', methods=['GET'])
def getGroups():
    groups = models.Group.query.all()
    json = {'groups': groups}

    return jsonify(json)

#
# Concrete group lessons by groupId
#

@app.route(defaultPath + 'groups/<int:groupId>', methods=['GET'])
def getGroup(groupId):
    lessons = models.Lesson.query.filter(models.Lesson.groupId == groupId).all()
    json = {'lessons': lessons}

    return jsonify(json)

#
# List of all lectors
#

@app.route(defaultPath + 'lectors', methods=['GET'])
def getLectors():
    lectors = models.Lector.query.all()
    json = {'lectors': lectors}

    return jsonify(json)

@app.route(defaultPath + 'lectors/<int:lectorId>', methods=['GET'])
def getLector(lectorId):
    lectors = models.Lector.query.filter(models.Lector.id == lectorId).first()
    if lectors != None:
        return jsonify(lectors)
    else:
        abort(404)
