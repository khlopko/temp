#!flask/bin/python

from app import models, db


class GroupsContent:

    def __init__(self):
        self.helper = GroupsHelper()

    def all(self):
        return models.Group.query.all()

    def add(self, group):
        if self.helper.is_exists(group):
            return GroupProcessCode.already_exists
        db.session.add(group)
        db.session.commit()
        return GroupProcessCode.ok

    def delete(self, group):
        group.delete()
        db.session.commit()
        return GroupProcessCode.ok

    def get(self, groupId):
        groups = self.all()
        group = next(group for group in groups if group.id == groupId)
        if group is None:
            return GroupProcessCode.no_such_group
        return group


class GroupsHelper:

    def is_exists(self, group):
        group = models.Group.query.filter(
            models.Group.title == group.title,
            models.Group.course == group.course).first()
        return group is not None


class GroupProcessCode:
    ok = -600
    already_exists = 677
    no_such_group = 680
