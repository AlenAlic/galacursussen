from flask import jsonify, request, json
from flask_login import login_required
from backend import db
from backend.admin import bp
from backend.models import User
from backend.values import *


@bp.route('/users', methods=[GET])
@login_required
def users():
    u = User.query.order_by(User.first_name).all()
    return jsonify([user.admin_json() for user in u])


@bp.route('/user/<int:user_id>', methods=[PATCH])
@login_required
def user(user_id):
    u = User.query.filter(User.user_id == user_id).first()
    form = json.loads(request.data)
    u.first_name = form["first_name"]
    u.last_name = form["last_name"]
    u.email = form["email"]
    u.incie = form["incie"]
    u.salcie = form["salcie"]
    u.mucie = form["mucie"]
    u.is_active = form["is_active"]
    u.active_member = form["active_member"]
    u.access = form["access"]
    db.session.commit()
    return OK