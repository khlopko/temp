#!flask/bin/python

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, models
from forms import *
from models import User, Role

#
# Index page.
#

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Miguel' }
    return render_template("index.html",
        title = 'Home',
        user = user)

#
# Login.
#

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/groups/<int:groupId>', methods=['GET'])
def groups(groupId):
    group = models.Group.query.filter(models.Group.id == groupId).first()
    lessons = models.Lesson.query.filter(models.Lesson.groupId == groupId).all()
    for lesson in lessons:
        print lesson.dayOfWeek
    return render_template(
        'group.html',
        title = 'Group ' + group.title,
        group = group,
        lessons = lessons,
        reverseDays = dict((v,k) for k,v in models.days.iteritems()))

#
# Lessons.
#

@app.route('/lessons/create/<int:groupId>', methods=['GET'])
def createLesson(groupId):
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

@app.route('/lessons/create/', methods=['POST'])
def create():
    json = request.form
    print(json)
    title = json.get('title')
    room = json['room']
    dayOfWeek = models.days[json['dayOfWeek']]
    print dayOfWeek
    position = json['position']
    weekNumber = json['weekNumber']
    lectorId = json['lectorId']
    groupId = json['groupId']
    lesson = models.Lesson(
        title = title,
        room = room,
        dayOfWeek = dayOfWeek,
        position = position,
        weekNumber = weekNumber,
        lectorId = lectorId,
        groupId = groupId)
    db.session.add(lesson)
    db.session.commit()
    return redirect('/groups/' + groupId)

#
# Admin panel
#

@app.route('/adminpanel', methods=['GET', 'POST'])
def adminpanel():
    addGroupForm = AddGroupForm()
    addLectorForm = AddLectorForm()
    if addGroupForm.validate_on_submit():
        return handleGroupAdd(addGroupForm)
    if addLectorForm.validate_on_submit():
        return handleLectorAdd(addLectorForm)
    return render_template(
        'adminpanel.html',
        models = models,
        addGroupForm = addGroupForm,
        addLectorForm = addLectorForm,
        redirect = redirect)

def handleGroupAdd(form):
    group = models.Group(title=form.titleField.data)
    db.session.add(group)
    db.session.commit()
    return redirect('/adminpanel')

def handleLectorAdd(form):
    lector = models.Lector(
        firstname=form.firstname.data,
        lastname=form.lastname.data, 
        sorname=form.sorname.data)
    db.session.add(lector)
    db.session.commit()
    return redirect('/adminpanel')
