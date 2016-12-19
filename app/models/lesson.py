#!flask/bin/python

from app import db
from days import days
from global_keys import Key


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(96), nullable=False)
    info = db.relationship('LessonInfo', backref='lesson', lazy='dynamic')
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    lector_id = db.Column(db.Integer, db.ForeignKey('lectors.id'), nullable=False)

    def __repr__(self):
        return '<Lesson %r :: %r>' % (self.title, self.info.all())

    @staticmethod
    def parse(json):
        title = json[Key.title]
        lector_id = int(json[Key.lector_id])
        group_id = int(json[Key.group_id])
        room = json[Key.room]
        day_of_week = days[json[Key.day_of_week]]
        position = int(json[Key.position])
        week_number = int(json[Key.week_number])
        
        lesson = Lesson(title=title, lector_id=lector_id, group_id=group_id)
        info = LessonInfo(
            room=room,
            day_of_week=day_of_week, position=position, week_number=week_number)

        return lesson, info

    def serialized(self):
        return {
            Key.id: self.id,
            Key.title: self.title,
            Key.lector: self.lector.serialized(),
            Key.info: map(LessonInfo.serialized, self.info)
        }


class LessonInfo(db.Model):
    __tablename__ = 'lessons_info'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    room = db.Column(db.String(16), nullable=False)
    day_of_week = db.Column(db.SmallInteger, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)

    def __repr__(self):
        return '<LessonInfo in %r: %r / %r / %r>' \
            % (self.room, self.day_of_week, self.position, self.week_number)

    def serialized(self):
        return {
            Key.room: self.room,
            Key.day_of_week: self.day_of_week,
            Key.week_number: self.week_number,
            Key.position: self.position,
        }
