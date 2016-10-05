#!flask/bin/python

from app import models, db


class LessonsContent:

    def __init__(self):
        self.group = None
        self.groupLessons = []
        self.helper = LessonsHelper()

    def set_group(self, group):
        self.group = group
        self.groupLessons = self.all_for_group(group)

    def all_at_day(self, day):
        lessons = [
            lesson for lesson in self.groupLessons if lesson.dayOfWeek == day
        ]
        return lessons

    def all_for_group(self, groupId):
            orderKey = models.Lesson.dayOfWeek
            predicate = models.Lesson.groupId == groupId
            lessons = models.Lesson.query.filter(predicate).order_by(orderKey).all()
            if lessons is None:
                return LessonProcessCode.bad_request
            return lessons

    def create_from_json(self, json):
        title = json['title']
        room = json['room']
        dayOfWeek = models.days[json['dayOfWeek']]
        position = json['position']
        weekNumber = json['weekNumber']
        lectorId = json['lectorId']
        groupId = json['groupId']
        lesson = models.Lesson(
            title=title, room=room,
            dayOfWeek=dayOfWeek, position=position, weekNumber=weekNumber,
            lectorId=lectorId, groupId=groupId)

        code = self.helper.is_exists(lesson)
        if code == LessonProcessCode.ok:
            db.session.add(lesson)
            db.session.commit()
        return code


class LessonsHelper:

    def is_exists(self, lesson):
        if_room = models.Lesson.room == lesson.room
        if_position = models.Lesson.position == lesson.position
        if_weekNumber = models.Lesson.weekNumber == lesson.weekNumber
        if_dayOfWeek = models.Lesson.dayOfWeek == lesson.dayOfWeek
        if_lector = models.Lesson.lectorId == lesson.lectorId
        if_group = models.Lesson.groupId == lesson.groupId
        common_check = if_position and if_dayOfWeek and if_weekNumber

        room_is_busy = models.Lesson.query.filter(if_room, common_check).first()
        if room_is_busy is not None:
            return LessonProcessCode.room_is_busy

        lector_is_busy = models.Lesson.query.filter(if_lector, common_check).first()
        if lector_is_busy is not None:
            return LessonProcessCode.lector_is_busy

        group_is_busy = models.Lesson.query.filter(if_group, common_check).first()
        if group_is_busy is not None:
            return LessonProcessCode.group_is_busy

        return LessonProcessCode.ok


class LessonProcessCode:
    ok = -500
    bad_request = 540
    room_is_busy = 553
    lector_is_busy = 563
    group_is_busy = 573
