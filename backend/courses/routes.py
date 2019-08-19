from flask import request, jsonify, json
from flask_login import login_required, current_user
from backend.courses import bp
from backend import db
from backend.models import new_courses_form_data, Course, AssignmentRequest, User, Attendance
from backend.values import *
from backend.courses.forms import AddCourseForm
from backend.responses import json_error, json_forbidden
from sqlalchemy import func
from datetime import datetime


@bp.route('/', methods=[GET, POST])
def index():
    courses = [c.json() for c in Course.query.filter(func.year(Course.date) > (func.year(datetime.now()) - 1)).all()]
    return jsonify(courses)


@bp.route('/new', methods=[GET, POST])
@login_required
def new():
    form = AddCourseForm()
    if request.method == GET:
        return new_courses_form_data()
    if request.method == POST:
        if form.validate():
            return Course.create(form.model_data()).course_added()
        else:
            return json_error(form.vue_error_form())


@bp.route('attend', methods=[POST])
@login_required
def attend():
    form = json.loads(request.data)
    assignment_request = AssignmentRequest.query.join(Course, User)\
        .filter(Course.course_id == form["course_id"], User.user_id == form["user_id"]).first()
    if assignment_request.user == current_user or current_user.is_admin() or current_user.is_organizer():
        assignment_request.attendance = Attendance[form["attendance"]]
        assignment_request.notes = form["notes"]
        db.session.commit()
        if current_user == assignment_request.user:
            return jsonify(f"Attendance set for {assignment_request.course.course_description()}.")
        return jsonify(f"Set {assignment_request.user.first_name} as {assignment_request.attendance.name} for "
                       f"{assignment_request.course.course_description()}.")
    return json_forbidden("You are not allowed to change this.")
