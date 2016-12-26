#!flask/bin/python

from flask import render_template, redirect, request
from app import db, models, title, jsonify
from forms import *
from errors_helper import StatusCode, ErrorHelper
from groups import GroupsContent
from lessons import LessonsContent
from models.days import days
from models.group import Group
from models.lector import Lector
from models.week_number import WeekNumber


groupsContent = GroupsContent()
lessonsContent = LessonsContent()


def index():
    
    return render_template(
        'index.html',
        title=title,
        groups=groupsContent.all(),
        dayKeys=sorted(days, key=days.__getitem__),
        dayValues=sorted(days.values()),
        helper=lessonsContent)


def groups(groupId):
    group = groupsContent.get(groupId)

    if type(group) is not Group:
        return jsonify(ErrorHelper.make_response_for_code(group))

    lessons = group.lessons

    return render_template(
        'group.html',
        title='Group ' + group.title,
        group=group,
        lessons=lessons,
        reverseDays=dict((v, k) for k, v in days.iteritems()))


def createLesson(groupId):
    if request.method == 'GET':
        return render_create_lesson(groupId)

    if request.method == 'POST':
        json = {}
        if request.headers['Content-Type'] == 'application/json':
            json = request.get_json().copy()
        elif 'multipart/form-data' in request.headers['Content-Type']:
            json = request.form.copy()
        else:
            abort(400)
        json['group_id'] = groupId
        code = lessonsContent.create_from_json(json)

        return jsonify(ErrorHelper.make_response_for_code(code))


def render_create_lesson(groupId):

    return render_template(
        'create_lesson.html',
        title='Create new lesson',
        group=groupsContent.get(groupId),
        lectors=sorted(Lector.query.all()),
        weeks=[WeekNumber.first, WeekNumber.second],
        days=sorted(days, key=days.__getitem__))


def adminpanel():
    addGroupForm = AddGroupForm()
    addLectorForm = AddLectorForm()

    if addGroupForm.validate_on_submit():
        group = Group(
            title=addGroupForm.title.data,
            course=addGroupForm.course.data)
        code = groupsContent.add(group)
        if code == StatusCode.ok:
            return redirect('/adminpanel')

    if addLectorForm.validate_on_submit():
        lector = Lector(
            firstname=addLectorForm.firstname.data,
            lastname=addLectorForm.lastname.data,
            sorname=addLectorForm.sorname.data)
        db.session.add(lector)
        db.session.commit()

        return redirect('/adminpanel')

    return render_template(
        'adminpanel.html',
        title='Admin Panel',
        groups=Group.query.all(),
        lectors=Lector.query.all(),
        addGroupForm=addGroupForm,
        addLectorForm=addLectorForm)
