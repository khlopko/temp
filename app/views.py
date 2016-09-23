#!flask/bin/python

from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, models, title
from forms import *
from operator import itemgetter

#
# Index page view.
#

def index():
    groups = models.Group.query.all()

    return render_template(
        'index.html',
        title = title,
        groups = groups,
        dayKeys = sorted(models.days, key = models.days.__getitem__),
        dayValues = sorted(models.days.values()),
        helper = IndexViewHelper())

class IndexViewHelper:

    def __init__(self):
        self.group = None
        self.groupLessons = []

    def setGroup(self, group):
        self.group = group
        self.groupLessons = models.Lesson.query.filter(models.Lesson.groupId == group.id).order_by(models.Lesson.dayOfWeek).all()

    def getLessons(self, day):
        lessons = [lesson for lesson in self.groupLessons if lesson.dayOfWeek == day]
        return lessons


#
# Login.
#

def login():
    
    form = LoginForm()
    
    if form.validate_on_submit():
        return redirect('/adminpanel')
    
    return render_template(
        'login.html',
        title = 'Sign In',
        form = form)

#
# Groups.
#

def groups(groupId):

    group = models.Group.query.filter(models.Group.id == groupId).first()
    lessons = models.Lesson.query.filter(models.Lesson.groupId == groupId).all()
    
    return render_template(
        'group.html',
        title = 'Group ' + group.title,
        group = group,
        lessons = lessons,
        reverseDays = dict((v,k) for k,v in models.days.iteritems()))

#
# Lessons.
#

def createLesson(groupId):

    if request.method == 'GET':
        group = models.Group.query.filter(models.Group.id == groupId).first()
        lectors = sorted(models.Lector.query.all())
        weeks = [models.WeekNumber.first, models.WeekNumber.second]
        return render_template(
            'create_lesson.html',
            title = 'Create new lesson',
            group = group,
            lectors = lectors,
            weeks = weeks,
            days = sorted(models.days, key=models.days.__getitem__))

    if request.method == 'POST':
        json = request.form
        title = json.get('title')
        room = json['room']
        dayOfWeek = models.days[json['dayOfWeek']]
        position = json['position']
        weekNumber = json['weekNumber']
        lectorId = json['lectorId']
        groupId = json['groupId']
        lesson = models.Lesson(
            title = title, room = room,
            dayOfWeek = dayOfWeek, position = position, weekNumber = weekNumber,
            lectorId = lectorId, groupId = groupId)
        db.session.add(lesson)
        db.session.commit()
        return redirect('/groups/' + groupId)

#
# Admin panel
#

def adminpanel():
    
    addGroupForm = AddGroupForm()
    addLectorForm = AddLectorForm()
    
    if addGroupForm.validate_on_submit():
        group = models.Group(title=addGroupForm.titleField.data)
        db.session.add(group)
        db.session.commit()
        return redirect('/adminpanel')
    
    if addLectorForm.validate_on_submit():
        lector = models.Lector(
            firstname=addLectorForm.firstname.data,
            lastname=addLectorForm.lastname.data, 
            sorname=addLectorForm.sorname.data)
        db.session.add(lector)
        db.session.commit()
        return redirect('/adminpanel')
    
    return render_template(
        'adminpanel.html',
        title = 'Admin Panel',
        models = models,
        addGroupForm = addGroupForm,
        addLectorForm = addLectorForm)    
