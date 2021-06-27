from backend import db, login, Anonymous
from flask import current_app, jsonify
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from backend.values import *
from time import time
import jwt
from datetime import datetime, timedelta
from functools import wraps
import enum
from backend.util import datetime_browser_format, is_float
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


class TrackModifications(object):
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


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


class User(UserMixin, Anonymous, db.Model, TrackModifications):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    reset_index = db.Column(db.Integer, nullable=False, default=0)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    access = db.Column(db.Integer, index=True, nullable=False)
    is_active = db.Column(db.Boolean, index=True, nullable=False, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    incie = db.Column(db.Boolean, nullable=False, default=False)
    salcie = db.Column(db.Boolean, nullable=False, default=False)
    mucie = db.Column(db.Boolean, nullable=False, default=False)
    auth_code = db.Column(db.String(128), nullable=True)
    email_notifications = db.Column(db.Boolean, nullable=False, default=True)
    assignments = db.relationship("Assignment", back_populates="user")
    active_member = db.Column(db.Boolean, index=True, nullable=False, default=True)

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

    def access_level(self):
        return ACCESS_LEVEL[self.access]

    def allowed(self, access_level):
        return self.access == access_level

    def set_password(self, password, increment=True):
        self.password_hash = generate_password_hash(password)
        if self.reset_index is not None and increment:
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
                "id": self.user_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "full_name": self.full_name(),
                "email": self.email,
                "access_level": self.access_level(),
                "admin": self.is_admin(),
                "organizer": self.is_organizer(),
                "member": self.is_member(),
                "treasurer": self.is_treasurer(),
                "incie": self.incie,
                "salcie": self.salcie,
                "mucie": self.mucie,
                "email_notifications": self.email_notifications
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

    @staticmethod
    def years_courses(year=None):
        return Course.courses_year_query(year).all()

    def years_assignment(self, year=None):
        return Assignment.assignments_year_query(year, self).all()

    def committee_assignments(self, year=None, committee=None):
        assignments = [a for a in self.years_assignment(year) if a.assigned]
        if committee == INCIE:
            assignments = [a for a in assignments if a.course.committee == Committee.incie and a.role != Role.mucie]
        elif committee == SALCIE:
            assignments = [a for a in assignments if a.course.committee == Committee.salcie and a.role != Role.mucie]
        elif committee == MUCIE:
            assignments = [a for a in assignments if a.role == Role.mucie]
        return assignments

    def hours(self, year=None, committee=None):
        courses = [a.course for a in self.committee_assignments(year, committee) if not a.course.cancelled]
        seconds = sum([c.duration for c in courses], timedelta()).seconds
        return datetime.utcfromtimestamp(seconds).strftime('%H:%M')

    def hours_breakdown(self, year=None, committee=None):
        assignments = self.committee_assignments(year, committee)
        seconds = sum([a.course.duration for a in assignments], timedelta()).seconds
        data = {"assignments": [a.hours() for a in assignments]}
        data.update({"total": datetime.utcfromtimestamp(seconds).strftime('%H:%M')})
        return data

    def json(self):
        return {
            "id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name(),
            "hours": self.hours()
        }

    def admin_json(self):
        return {
            "id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name(),
            "email": self.email,
            "access_level": self.access_level(),
            "incie": self.incie,
            "salcie": self.salcie,
            "mucie": self.mucie,
            "is_active": self.is_active,
            "active_member": self.active_member,
            "access": self.access
        }

    def created(self):
        return f"Created account for {self.full_name()} ({self.email})."


class Language(enum.Enum):
    nl = "Dutch"
    en = "English"
    unknown = "Unknown"


class Committee(enum.Enum):
    incie = "InCie"
    salcie = "SalCie"


class Course(db.Model, TrackModifications):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, primary_key=True)
    requested_by = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime)
    duration = db.Column(db.Interval)
    attendees = db.Column(db.Integer)
    location = db.Column(db.String(256))
    language = db.Column(db.Enum(Language), nullable=False, default=Language.unknown)
    committee = db.Column(db.Enum(Committee), nullable=False)
    price = db.Column(db.Float)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    dances = db.Column(db.String(256))
    notes = db.Column(db.String(256))
    cancelled = db.Column(db.Boolean, nullable=False, default=False)
    assignments = db.relationship("Assignment", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return self.requested_by

    def name(self):
        return f"Course for {self.course_date()}"

    def course_description(self):
        ending = self.date + self.duration
        return f"{self.requested_by} on {self.date.strftime('%A %d %B')}, from " \
            f"{self.date.strftime('%H:%M')} to {ending.strftime('%H:%M')}"

    def course_added(self):
        return jsonify(f"Added course for {self.course_description()}")

    def changes_saved(self):
        return jsonify(f"Saved changes for {self.course_description()}")

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
    def courses_year_query(year=None):
        if year is not None:
            start_date = datetime(year, FIRST_MONTH, 1)
            end_date = datetime(year + 1, FIRST_MONTH, 1)
        else:
            offset = 0 if datetime.now().month >= FIRST_MONTH else -1
            start_date = datetime(datetime.now().year + offset, FIRST_MONTH, 1)
            end_date = datetime(datetime.now().year + offset + 2, FIRST_MONTH, 1)
        return Course.query.filter(Course.date >= start_date, Course.date < end_date).order_by(Course.date)

    @staticmethod
    def parse_dates(data):
        data["date"] = datetime.strptime(data["date"], DATETIME_FORMAT)
        duration = datetime.strptime(data["duration"], DATETIME_FORMAT)
        data["duration"] = timedelta(hours=duration.hour, minutes=duration.minute)
        return data

    @staticmethod
    def generate_assignments(course):
        users = User.query.filter(User.active_member.is_(True))
        if course.committee == Committee.incie.name:
            users = users.filter(or_(User.mucie.is_(True), User.incie.is_(True)))
        if course.committee == Committee.salcie.name:
            users = users.filter(or_(User.mucie.is_(True), User.salcie.is_(True)))
        users = users.all()
        for u in users:
            assignment = Assignment()
            assignment.user = u
            assignment.course = course

    def save(self, data, patch=False):
        if patch:
            data = self.parse_dates(data)
        course = Course() if not patch else self
        course.requested_by = data["requested_by"]
        course.date = data["date"]
        course.duration = data["duration"]
        course.location = data["location"]
        course.language = data["language"]
        course.committee = data["committee"]
        course.dances = data["dances"]
        course.notes = data["notes"]
        if patch:
            for change in data["assignments"]:
                req = Assignment.query.filter(Assignment.assignment_id == change).first()
                req.attendance = data["assignments"][change]
            if data["attendees"] != "":
                course.attendees = data["attendees"]
            else:
                course.attendees = None
            if is_float(data["price"]):
                course.price = float(data["price"])
            course.paid = data["paid"]
        else:
            self.generate_assignments(course)
            db.session.add(course)
        db.session.commit()
        return course

    def json(self):
        return {
            "key": str(datetime.now()),
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
            "language_value": self.language.name,
            "committee_value": self.committee.name,
            "price": self.price,
            "paid": self.paid,
            "dances": self.dances,
            "notes": self.notes,
            "cancelled": self.cancelled,
            "assignments": list(sorted([a.json() for a in self.assignments], key=lambda x: x["name"].lower())),
            "responses": len([r for r in self.assignments if r.attendance is not None]),
            "has_mucie": len([r for r in self.assignments
                              if r.attendance == Attendance.yes and r.user.mucie]) > 0
        }


class Attendance(enum.Enum):
    yes = "Yes"
    maybe = "Maybe"
    no = "No"


class Role(enum.Enum):
    teacher = "Teacher"
    assistant = "Assistant"
    mucie = "MuCie"


class Assignment(db.Model, TrackModifications):
    __tablename__ = "assignment"
    assignment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', onupdate="CASCADE", ondelete="CASCADE"))
    user = db.relationship("User", back_populates="assignments")
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id', onupdate="CASCADE", ondelete="CASCADE"))
    course = db.relationship("Course", back_populates="assignments")
    attendance = db.Column(db.Enum(Attendance))
    notes = db.Column(db.String(256))
    role = db.Column(db.Enum(Role))
    assigned = db.Column(db.Boolean)

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

    def assignment(self):
        return f"Assigned {self.user.first_name} to {self.course}." if self.assigned else self.removed()

    def set_role(self):
        return f"Set {self.user.first_name} as {self.role.value if self.role is not None else 'general member'}."

    def removed(self):
        return f"Removed {self.user.first_name} from {self.course}."

    def committee(self):
        return self.course.committee == Committee.incie and self.user.incie or \
               self.course.committee == Committee.salcie and self.user.salcie

    @staticmethod
    def assignments_year_query(year=None, user=user):
        if year is not None:
            start_date = datetime(year, FIRST_MONTH, 1)
            end_date = datetime(year + 1, FIRST_MONTH, 1)
        else:
            offset = 0 if datetime.now().month >= FIRST_MONTH else -1
            start_date = datetime(datetime.now().year + offset, FIRST_MONTH, 1)
            end_date = datetime(datetime.now().year + offset + 1, FIRST_MONTH, 1)
        return Assignment.query.join(Course).filter(Course.date >= start_date, Course.date < end_date,
                                                    Assignment.user == user)

    def role_formatted(self):
        return self.role.value if self.role is not None else ""

    def json(self):
        return {
            "id": self.assignment_id,
            "user_id": self.user.user_id,
            "name": self.user.full_name(),
            "attendance": self.attendance.name if self.attendance is not None else None,
            "notes": self.notes,
            "mucie": self.user.mucie,
            "role": self.role.value if self.role is not None else None,
            "assigned": self.assigned,
            "has_teacher": any([a.role == Role.teacher for a in self.course.assignments]),
            "has_assistant": any([a.role == Role.assistant for a in self.course.assignments]),
            "has_mucie": any([a.role == Role.mucie for a in self.course.assignments]),
            "committee": self.committee(),
            "hours": self.user.hours()
        }

    def hours(self):
        return {
            "id": self.assignment_id,
            "requested_by": self.course.requested_by,
            "date_formatted": self.course.date_formatted(),
            "duration_formatted": self.course.duration_formatted(),
        }
