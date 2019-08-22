from flask import request, jsonify, json
from flask_login import login_required, current_user
from backend.courses import bp
from backend import db
from backend.models import new_courses_form_data, Course, User, Attendance, Assignment
from backend.values import *
from backend.courses.forms import AddCourseForm
from backend.responses import json_error, json_forbidden
from datetime import datetime


@bp.route('/', methods=[GET], defaults={'year': None})
@bp.route('/<int:year>', methods=[GET])
@login_required
def index(year):
    if year is not None:
        start_date = datetime(year, FIRST_MONTH, 1)
        end_date = datetime(year+1, FIRST_MONTH, 1)
        courses = Course.query.filter(Course.date >= start_date, Course.date < end_date).all()
        c = {c.course_id: c.json() for c in courses}
        return jsonify(c)
    offset = 0 if datetime.now().month >= FIRST_MONTH else -1
    start_date = datetime(datetime.now().year + offset, FIRST_MONTH, 1)
    end_date = datetime(datetime.now().year + offset + 1, FIRST_MONTH, 1)
    courses = Course.query.filter(Course.date >= start_date, Course.date < end_date).all()
    c = {c.course_id: c.json() for c in courses}
    return jsonify(c)


@bp.route('/updated/<int:course_id>', methods=[GET, PATCH])
@login_required
def updated(course_id):
    if request.method == GET:
        return jsonify(Course.query.filter(Course.course_id == course_id).first().json())
    if request.method == PATCH:
        course = Course.query.filter(Course.course_id == course_id).first()
        course.save(json.loads(request.data), patch=True)
        return course.changes_saved()


@bp.route('/new', methods=[GET, POST])
@login_required
def new():
    form = AddCourseForm()
    if request.method == GET:
        return new_courses_form_data()
    if request.method == POST:
        if form.validate():
            course = Course()
            return course.save(form.model_data()).course_added()
        else:
            return json_error(form.vue_error_form())


@bp.route('attend', methods=[PATCH])
@login_required
def attend():
    form = json.loads(request.data)
    assignment = Assignment.query.join(Course, User)\
        .filter(Course.course_id == form["course_id"], User.user_id == form["user_id"]).first()
    if assignment.user == current_user or current_user.is_admin() or current_user.is_organizer():
        assignment.attendance = Attendance[form["attendance"]]
        assignment.notes = form["notes"]
        db.session.commit()
        if current_user == assignment.user:
            return jsonify(f"Attendance set for {assignment.course.course_description()}.")
        return jsonify(f"Set {assignment.user.first_name} as {assignment.attendance.name} for "
                       f"{assignment.course.course_description()}.")
    return json_forbidden("You are not allowed to change this.")


@bp.route('/assign/<int:assignment_id>', methods=[PATCH])
@login_required
def assign(assignment_id):
    data = json.loads(request.data)
    assignment = Assignment.query.filter(Assignment.assignment_id == assignment_id).first()
    assignment.assigned = data["assigned"]
    if not assignment.assigned:
        assignment.role = None
    db.session.commit()
    return jsonify({"message": assignment.assignment(), "course": assignment.course.json()})


@bp.route('/role/<int:assignment_id>', methods=[PATCH])
@login_required
def role(assignment_id):
    data = json.loads(request.data)
    assignment = Assignment.query.filter(Assignment.assignment_id == assignment_id).first()
    assignment.role = data["role"]
    db.session.commit()
    return jsonify({"message": assignment.set_role(), "course": assignment.course.json()})
