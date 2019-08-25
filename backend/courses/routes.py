from flask import request, jsonify, json
from flask_login import login_required, current_user
from backend.courses import bp
from backend import db
from backend.models import new_courses_form_data, Course, User, Attendance, Assignment
from backend.values import *
from backend.courses.forms import AddCourseForm
from backend.responses import json_error, json_forbidden


@bp.route('/', methods=[GET], defaults={'year': None})
@bp.route('/<int:year>', methods=[GET])
@login_required
def index(year):
    courses = Course.courses_year_query(year).all()
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
        return OK


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


@bp.route('/paid/<int:course_id>', methods=[PATCH])
@login_required
def paid(course_id):
    data = json.loads(request.data)
    course = Course.query.filter(Course.course_id == course_id).first()
    course.paid = data["paid"]
    db.session.commit()
    return OK


def calculate_hours(year, u):
    i = u.hours_breakdown(year=year, committee=INCIE)
    s = u.hours_breakdown(year=year, committee=SALCIE)
    m = u.hours_breakdown(year=year, committee=MUCIE)
    c = {}
    if len(i["assignments"]) > 0 or u.incie:
        c.update({INCIE: i})
    if len(s["assignments"]) > 0 or u.salcie:
        c.update({SALCIE: s})
    if len(m["assignments"]) > 0 or u.mucie:
        c.update({MUCIE: m})
    return c


@bp.route('/hours/<int:year>', methods=[GET])
@login_required
def hours(year):
    c = calculate_hours(year, current_user)
    return jsonify(c)


def calculate_total_hours(year, u):
    i = u.hours(year=year, committee=INCIE)
    s = u.hours(year=year, committee=SALCIE)
    m = u.hours(year=year, committee=MUCIE)
    c = {}
    if i != "00:00" or u.incie:
        c.update({INCIE: i})
    else:
        c.update({INCIE: "-"})
    if s != "00:00" or u.salcie:
        c.update({SALCIE: s})
    else:
        c.update({SALCIE: "-"})
    if m != "00:00" or u.mucie:
        c.update({MUCIE: m})
    else:
        c.update({MUCIE: "-"})
    return c


@bp.route('/total_hours/<int:year>', methods=[GET])
def total_hours(year):
    users = User.query.filter(User.access != ACCESS[TREASURER]).order_by(User.first_name).all()
    c = [{"user": u.full_name(), "hours": calculate_total_hours(year, u)} for u in users]
    return jsonify(c)
