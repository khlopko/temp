#!flask/bin/python

from app import db
from models.group import Group
from errors_helper import StatusCode
from models.global_keys import Key


class GroupsContent:

    def __init__(self):
        self.helper = GroupsHelper()

    def all(self):
        return Group.query.all()

    def add(self, group):
        if self.helper.is_exists(group):
            return (None, StatusCode.already_exists)
        db.session.add(group)
        db.session.commit()

        return (group, StatusCode.ok)

    def add_from_json(self, json):
        title = str(json[Key.title])
        course = int(json[Key.course])
        group = Group(title=title, course=course)

        return self.add(group)

    def delete(self, group):
        group.delete()
        db.session.commit()

        return StatusCode.ok

    def get(self, group_id):
        groups = self.all()
        if group_id is None:
            group_id = 1
        
        if not groups:
            return StatusCode.not_found

        group = [g for g in groups if g.id == group_id][0]
        if group is None:
            return StatusCode.not_found

        return group


class GroupsHelper:

    def is_exists(self, group):
        group = Group.query.filter(
            Group.title == group.title,
            Group.course == group.course).first()
        
        return group is not None
