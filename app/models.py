#!flask/bin/python

from app import db

#
# Weekday of lesson.
#

class DayOfWeek(object):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6

#
# Week of lesson.
#

class WeekNumber(object):
    first = 0
    second = 1

#
# Lesson model.
#

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(128))
    room = db.Column(db.String(32))
    dayOfWeek = db.Column(db.SmallInteger)
    position = db.Column(db.Integer)
    weekNumber = db.Column(db.Integer)
    lectorId = db.Column(db.Integer, db.ForeignKey('lector.id'))
    groupId = db.Column(db.Integer, db.ForeignKey('group.id'))

    def __repr__(self):
        return '<Lesson %r>' % (self.title)

#
# Lector model.
#

class Lector(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(128), index = True, unique = True)
    sorname = db.Column(db.String(128), index = True, unique = True)
    lastname = db.Column(db.String(128), index = True, unique = True)
    lessons = db.relationship('Lesson', backref = 'lector', lazy = 'dynamic')

    def __repr__(self):
        return '<Lector %r>' % (self.firstname)

#
# Group model.
#

class Group(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), index = True, unique = True)
    lessons = db.relationship('Lesson', backref = 'group', lazy = 'dynamic')

    def __repr__(self):
        return '<Group %r>' % (self.title)

#
# User's role.
#

class Role(object):
    watcher = 0
    admin = 42

#
# User model.
#

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    firstname = db.Column(db.String(128), index = True, unique = True)
    sorname = db.Column(db.String(128), index = True, unique = True)
    lastname = db.Column(db.String(128), index = True, unique = True)
    role = db.Column(db.Integer, default = Role.watcher)

    def __repr__(self):
        return '<User %r>' % (self.username)
