from backend import db, login, Anonymous
from flask import current_app, jsonify
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from backend.values import *
from time import time
import jwt
from datetime import datetime
from functools import wraps
import enum
from backend.util import datetime_browser_format
from sqlalchemy import or_


def requires_access_level(access_levels):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.access not in access_levels:
                pass
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@login.request_loader
def load_user(request):
    try:
        token = request.headers.get("Authorization").replace("Bearer ", "")
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = data["id"]
        reset_index = data["reset_index"]
    except (jwt.exceptions.InvalidTokenError, AttributeError, KeyError):
        return None
    user = User.query.filter(User.user_id == user_id, User.reset_index == reset_index).first()
    return user if user is not None else None


class User(UserMixin, Anonymous, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    reset_index = db.Column(db.Integer, nullable=False, default=0)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    access = db.Column(db.Integer, index=True, nullable=False)
    is_active = db.Column(db.Boolean, index=True, nullable=False, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow())
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    incie = db.Column(db.Boolean, nullable=False, default=False)
    salcie = db.Column(db.Boolean, nullable=False, default=False)
    mucie = db.Column(db.Boolean, nullable=False, default=False)
    assignment_requests = db.relationship("AssignmentRequest", back_populates="user")
    assignments = db.relationship("Assignment", back_populates="user")

    def __repr__(self):
        return f'{self.email}'

    def get_id(self):
        return f"{self.user_id}-{self.reset_index}"

    def is_admin(self):
        return self.access == ACCESS[ADMIN]

    def is_organizer(self):
        return self.access == ACCESS[ORGANIZER]

    def is_member(self):
        return self.access == ACCESS[MEMBER]

    def is_treasurer(self):
        return self.access == ACCESS[TREASURER]

    def allowed(self, access_level):
        return self.access == access_level

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        if self.reset_index is not None:
            self.reset_index += 1
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.user_id, 'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except jwt.exceptions.InvalidTokenError:
            return 'error'
        return User.query.get(user_id)

    def profile(self):
        if current_user == self:
            return {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "full_name": self.full_name(),
                "email": self.email,
                "admin": self.is_admin(),
                "organizer": self.is_organizer(),
                "member": self.is_member(),
                "treasurer": self.is_treasurer()
            }
        return "Not logged in"

    def get_auth_token(self, expires_in=86400):
        return {
            "id": self.user_id,
            "token": jwt.encode(
                {'id': self.user_id,
                 "reset_index": self.reset_index,
                 "access": self.access,
                 'exp': time() + expires_in
                 }, current_app.config['SECRET_KEY'],  algorithm='HS256').decode('utf-8')
        }

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def json(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name(),
        }


class Configuration(db.Model):
    __tablename__ = "configuration"
    lock_id = db.Column(db.Integer, primary_key=True)
    maintenance = db.Column(db.Integer, default=False, nullable=False)


class Language(enum.Enum):
    nl = "Dutch"
    en = "English"
    unknown = "Unknown"


class Committee(enum.Enum):
    incie = "InCie"
    salcie = "SalCie"


def new_courses_form_data():
    return jsonify(
        {"languages": [{"value": i.name, "text": i.value} for i in Language],
         "committees": [{"value": i.name, "text": i.value} for i in Committee]
         })


class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key=True)
    requested_by = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime)
    duration = db.Column(db.Interval)
    attendees = db.Column(db.Integer, nullable=False, default=0)
    location = db.Column(db.String(256))
    language = db.Column(db.Enum(Language), nullable=False, default=Language.unknown)
    committee = db.Column(db.Enum(Committee), nullable=False)
    price = db.Column(db.Integer, nullable=False, default=0)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    dances = db.Column(db.String(256))
    notes = db.Column(db.String(256))
    cancelled = db.Column(db.Boolean, nullable=False, default=False)
    assignment_requests = db.relationship("AssignmentRequest", back_populates="course")
    assignments = db.relationship("Assignment", back_populates="course")

    def __repr__(self):
        return self.name()

    def name(self):
        return f"Course for {self.course_date()}"

    def course_description(self):
        ending = self.date + self.duration
        return f"{self.requested_by} on {self.date.strftime('%A %d %B')}, from " \
            f"{self.date.strftime('%H:%M')} to {ending.strftime('%H:%M')}"

    def course_added(self):
        return jsonify(f"Added course for {self.course_description()}")

    def json_date(self):
        return datetime_browser_format(self.date)

    def json_duration(self):
        return datetime_browser_format(datetime(1970, 1, 1, 0, 0, 0, 0) + self.duration)

    def date_formatted(self):
        ending = self.date + self.duration
        return f"{self.date.strftime('%A %d %B')}, {self.date.strftime('%H:%M')}-{ending.strftime('%H:%M')}"

    def duration_formatted(self):
        duration = datetime(1970, 1, 1, 0, 0, 0, 0) + self.duration
        return f"{duration.strftime('%H:%M')}"

    @staticmethod
    def create(data):
        course = Course()
        course.requested_by = data["requested_by"]
        course.date = data["date"]
        course.duration = data["duration"]
        course.location = data["location"]
        course.language = data["language"]
        course.committee = data["committee"]
        course.dances = data["dances"]
        course.notes = data["notes"]
        users = User.query.filter(User.is_active.is_(True))
        if course.committee == Committee.incie.name:
            users = users.filter(or_(User.mucie.is_(True), User.incie.is_(True)))
        if course.committee == Committee.salcie.name:
            users = users.filter(or_(User.mucie.is_(True), User.salcie.is_(True)))
        users = users.all()
        for u in users:
            assignment_request = AssignmentRequest()
            assignment_request.user = u
            assignment_request.course = course
        db.session.add(course)
        db.session.commit()
        return course

    def json(self):
        return {
            "id": self.course_id,
            "requested_by": self.requested_by,
            "date": self.json_date(),
            "date_formatted": self.date_formatted(),
            "date_description": self.course_description(),
            "duration": self.json_duration(),
            "duration_formatted": self.duration_formatted(),
            "attendees": self.attendees,
            "location": self.location,
            "language": self.language.value,
            "committee": self.committee.value,
            "price": self.price,
            "paid": self.paid,
            "dances": self.dances,
            "notes": self.notes,
            "assignment_requests": list(sorted([a.json() for a in self.assignment_requests], key=lambda x: x["name"])),
            "assignments": list(sorted([a.json() for a in self.assignments], key=lambda x: x["name"])),
            "responses": len([r for r in self.assignment_requests if r.attendance is not None]),
            "has_mucie": len([r for r in self.assignment_requests
                              if r.attendance == Attendance.yes and r.user.mucie]) > 0
        }


class Attendance(enum.Enum):
    yes = "Yes"
    maybe = "Maybe"
    no = "No"
    prefer = "Yes, with preference for teaching/assisting"


class AssignmentRequest(db.Model):
    __tablename__ = "assignment_request"
    assignment_request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', onupdate="CASCADE", ondelete="CASCADE"))
    user = db.relationship("User", back_populates="assignment_requests")
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id', onupdate="CASCADE", ondelete="CASCADE"))
    course = db.relationship("Course", back_populates="assignment_requests")
    attendance = db.Column(db.Enum(Attendance))
    notes = db.Column(db.String(256))

    def assignment_message(self):
        if self.attendance == Attendance.yes:
            return f"You can attend the course for {self.course.course_description()}"
        if self.attendance == Attendance.prefer:
            return f"You can attend the course for {self.course.course_description()}, and prefer to teach or assist " \
                f"the course."
        if self.attendance == Attendance.maybe:
            return f"You might be able to attend the course for {self.course.course_description()}"
        if self.attendance == Attendance.no:
            return f"You cannot attend the course for {self.course.course_description()}"
        return

    def json(self):
        return {
            "id": self.assignment_request_id,
            "user_id": self.user.user_id,
            "name": self.user.full_name(),
            "attendance": self.attendance.name if self.attendance is not None else None,
            "notes": self.notes,
            "mucie": self.user.mucie
        }


class Assignment(db.Model):
    __tablename__ = "assignment"
    assignment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', onupdate="CASCADE", ondelete="CASCADE"))
    user = db.relationship("User", back_populates="assignments")
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id', onupdate="CASCADE", ondelete="CASCADE"))
    course = db.relationship("Course", back_populates="assignments")
    mucie = db.Column(db.Boolean, nullable=False, default=False)
    teacher = db.Column(db.Boolean, nullable=False, default=False)
    assistant = db.Column(db.Boolean, nullable=False, default=False)

    def json(self):
        return {
            "id": self.assignment_id,
            "name": self.user.full_name(),
            "mucie": self.mucie,
            "teacher": self.teacher,
            "assistant": self.assistant
        }
