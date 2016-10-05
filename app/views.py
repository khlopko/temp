#!flask/bin/python

from flask import render_template, redirect, request
from app import db, models, title
from forms import *
from groups import GroupsContent, GroupProcessCode
from lessons import LessonsContent, LessonProcessCode


groupsContent = GroupsContent()
lessonsContent = LessonsContent()


def index():
    groups = groupsContent.all()

    return render_template(
        'index.html',
        title=title,
        groups=groups,
        dayKeys=sorted(models.days, key=models.days.__getitem__),
        dayValues=sorted(models.days.values()),
        helper=lessonsContent)


def groups(groupId):
    group = groupsContent.get(groupId)
    lessons = lessonsContent.all_for_group(groupId)

    return render_template(
        'group.html',
        title='Group ' + group.title,
        group=group,
        lessons=lessons,
        reverseDays=dict((v, k) for k, v in models.days.iteritems()))


def createLesson(groupId):
    if request.method == 'GET':
        group = groupsContent.get(groupId)
        lectors = sorted(models.Lector.query.all())
        weeks = [models.WeekNumber.first, models.WeekNumber.second]
        return render_template(
            'create_lesson.html',
            title='Create new lesson',
            group=group,
            lectors=lectors,
            weeks=weeks,
            days=sorted(models.days, key=models.days.__getitem__))

    if request.method == 'POST':
        json = request.form
        code = lessonsContent.create_from_json(json)
        print('ERROR HERE >>> ' + str(code))
        return redirect('/groups/' + str(groupId))


def adminpanel():

    addGroupForm = AddGroupForm()
    addLectorForm = AddLectorForm()

    if addGroupForm.validate_on_submit():
        group = models.Group(
            title=addGroupForm.title.data,
            course=addGroupForm.course.data)
        code = groupsContent.add(group)
        if code == GroupProcessCode.ok:
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
        title='Admin Panel',
        models=models,
        addGroupForm=addGroupForm,
        addLectorForm=addLectorForm)
