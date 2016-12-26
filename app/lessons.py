#!flask/bin/python

from app import models, db
from sqlalchemy import and_
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
        lesson, exists = self.helper.if_lesson(lesson)
        code = self.helper.is_exists(lesson, info)
        
        if code == StatusCode.ok:
            if not exists:
                db.session.add(lesson)
                db.session.commit()
            info.lesson_id = lesson.id
            db.session.add(info)
            db.session.commit()

            return (lesson, code)

        return (None, code)

    def delete(self, lesson_id):
        Lesson.query.filter(Lesson.id == lesson_id).delete()
        db.session.commit()
        return StatusCode.ok


class LessonsHelper:

    def if_lesson(self, lesson):
        queried = Lesson.query.filter(and_(
            Lesson.group_id == lesson.group_id, 
            Lesson.lector_id == lesson.lector_id,
            Lesson.title == lesson.title)).one_or_none()
        if queried is None:
            return (lesson, False)
        else:
            return (queried, True)

    def is_exists(self, lesson, info):
        common_check = Lesson.info.any(and_(
            LessonInfo.week_number == info.week_number,
            LessonInfo.position == info.position,
            LessonInfo.day_of_week == info.day_of_week))
        if_room = Lesson.info.any(LessonInfo.room == info.room)
        if_lector = Lesson.lector_id == lesson.lector_id
        if_group = Lesson.group_id == lesson.group_id
        
        group_is_busy = Lesson.query.filter(if_group, common_check).one_or_none()
        print group_is_busy
        if group_is_busy is not None:
            return StatusCode.group_is_busy
        
        room_is_busy = LessonInfo.query.filter(if_room, common_check).one_or_none()
        if room_is_busy is not None:
            return StatusCode.room_is_busy
        
        lector_is_busy = Lesson.query.filter(if_lector, common_check).one_or_none()
        if lector_is_busy is not None:
            return StatusCode.lector_is_busy

        return StatusCode.ok
