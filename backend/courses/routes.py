from flask import request, jsonify, json
from flask_login import login_required, current_user
from backend.courses import bp
from backend import db
from backend.models import Course, User, Attendance, Assignment, Committee
from backend.values import *
from backend.courses.forms import AddCourseForm
from backend.responses import json_error, json_forbidden, no_content
from sqlalchemy import func
from datetime import datetime
from backend.courses.email import send_reminder_email, send_assignments_email, send_cancellation_email


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


@bp.route('/new', methods=[POST])
@login_required
def new():
    form = AddCourseForm()
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
        if assignment.attendance == Attendance.no and assignment.assigned:
            assignment.assigned = False
            organizers = User.query.filter(User.access == ACCESS[ORGANIZER])
            for org in organizers:
                send_cancellation_email(org, assignment)
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
@login_required
def total_hours(year):
    users = User.query.filter(User.access != ACCESS[TREASURER]).order_by(func.lower(User.first_name)).all()
    users = [{"user": u, "hours": calculate_total_hours(year, u)} for u in users]
    users = [u for u in users if u["user"].active_member
             or (not u["hours"][INCIE] == "-" or not u["hours"][SALCIE] == "-" or not u["hours"][MUCIE] == "-")]
    users = [{"user": u["user"].full_name(), "hours": u["hours"]} for u in users]
    return jsonify(users)


def unresponsive_users():
    assignment = Assignment.query.join(Course).filter(Course.date > datetime.now(), Assignment.attendance.is_(None)) \
        .group_by(Assignment.user_id).all()
    return [a.user for a in assignment]


@bp.route('/notification', methods=[GET, POST])
@login_required
def notification():
    if request.method == GET:
        users = sorted([u.full_name() for u in unresponsive_users()], key=lambda x: x.lower())
        return jsonify(users)
    if request.method == POST:
        users = unresponsive_users()
        if len(users) > 0:
            for u in users:
                send_reminder_email(u)
            return ""
        else:
            return no_content


@bp.route('/assignments', methods=[POST])
@login_required
def assignments():
    all_courses = Course.query.filter(Course.date > datetime.now()).order_by(Course.committee, Course.date).all()
    if len(all_courses) > 0:
        incie_courses = [c for c in all_courses if c.committee == Committee.incie]
        salcie_courses = [c for c in all_courses if c.committee == Committee.salcie]
        users = User.query.filter(User.is_active.is_(True)).all()
        incie = [u for u in users if u.incie]
        salcie = [u for u in users if u.salcie]
        both = [u for u in users if (u.incie and u.salcie) or u.mucie]
        sent = []
        for u in both:
            if u not in sent:
                sent.append(u)
                send_assignments_email(u, incie_courses, salcie_courses, "mucie")
        for u in incie:
            if u not in sent:
                sent.append(u)
                send_assignments_email(u, incie_courses, [], "incie")
        for u in salcie:
            if u not in sent:
                sent.append(u)
                send_assignments_email(u, [], salcie_courses, "salcie")
        return ""
    else:
        return no_content
