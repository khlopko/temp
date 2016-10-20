#!flask/bin/python

from app import models, db
from models.lesson import Lesson, LessonInfo
from errors_helper import StatusCode


class LessonsContent:

    def __init__(self):
        self.group = None
        self.helper = LessonsHelper()

    def set_group(self, group):
        self.group = group

    def all_at_day(self, day):
        if self.group is None:
            return []

        def predicate(info): return [i for i in info if i.day_of_week == day] != []
        lessons = [lesson for lesson in self.group.lessons if predicate(lesson.info)]

        print lessons
        return lessons

    def create_from_json(self, json):
        lesson, info = Lesson.parse(json)
        code = self.helper.is_exists(lesson, info)
        if code == StatusCode.ok:
            db.session.add(lesson)
            db.session.commit()
            info.lesson_id = lesson.id
            db.session.add(info)
            db.session.commit()
        return code


class LessonsHelper:

    def is_exists(self, lesson, info):
        predicate = \
            LessonInfo.position == info.position and \
            LessonInfo.week_number == info.week_number and \
            LessonInfo.day_of_week == info.day_of_week
        common_check = Lesson.info.any(predicate)
        if_room = Lesson.info.any(LessonInfo.room == info.room)
        if_lector = Lesson.lector_id == lesson.lector_id
        if_group = Lesson.group_id == lesson.group_id

        group_is_busy = Lesson.query.filter(if_group, common_check).first()
        if group_is_busy is not None:
            return StatusCode.group_is_busy

        room_is_busy = LessonInfo.query.filter(if_room, common_check).first()
        if room_is_busy is not None:
            return StatusCode.room_is_busy

        lector_is_busy = Lesson.query.filter(if_lector, common_check).first()
        if lector_is_busy is not None:
            return StatusCode.lector_is_busy

        return StatusCode.ok
