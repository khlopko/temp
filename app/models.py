#!flask/bin/python

from app import db

#
# Weekday of lesson.
#

days = {
    'Monday': 0,
    'Tuesday': 1,
    'Wednesday': 2,
    'Thursday': 3,
    'Friday': 4,
    'Saturday': 5,
    'Sunday': 6
}

#
# Week of lesson.
#

class WeekNumber(object):
    first = 1
    second = 2

#
# Lesson model.
#

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    title = db.Column(db.String(128), nullable = False)
    room = db.Column(db.String(32), nullable = False)
    dayOfWeek = db.Column(db.SmallInteger, nullable = False)
    position = db.Column(db.Integer, nullable = False)
    weekNumber = db.Column(db.Integer, nullable = False)
    lectorId = db.Column(db.Integer, db.ForeignKey('lector.id'), nullable = False)
    groupId = db.Column(db.Integer, db.ForeignKey('group.id'), nullable = False)

    def __repr__(self):
        return '<Lesson %r>' % (self.title)

#
# Lector model.
#

class Lector(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    firstname = db.Column(db.String(128), index = True, nullable = False)
    sorname = db.Column(db.String(128), index = True, nullable = False)
    lastname = db.Column(db.String(128), index = True, nullable = False)
    lessons = db.relationship('Lesson', backref = 'lector', lazy = 'dynamic')

    def __repr__(self):
        return '<Lector %r>' % (self.firstname)

#
# Group model.
#

class Group(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    title = db.Column(db.String(64), index = True, unique = True, nullable = False)
    course = db.Column(db.Integer, index = True, nullable = False)
    lessons = db.relationship('Lesson', backref = 'group', lazy = 'dynamic')

    def __repr__(self):
        return '<Group %r>' % (self.title)
