from flask import jsonify, request, json
from flask_login import current_user, login_required
from backend.auth import bp
from backend.auth.forms import LoginForm
from backend.models import User
from backend.responses import json_unauthorized, json_error
from backend.values import *
from backend import db


@bp.route('/login', methods=[POST])
def login():
    form = LoginForm()
    if form.validate():
        user = User.query.filter(User.email == form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            return json_unauthorized("Invalid username or password")
        elif user.is_active:
            return jsonify(user.get_auth_token(expires_in=31536000 if form.remember_me.data else 86400))
        else:
            return json_unauthorized("Account inactive")
    return json_unauthorized(form.login_status())


@bp.route('/user/<int:user_id>', methods=[GET, PATCH])
@login_required
def user(user_id):
    u = User.query.filter(User.user_id == user_id).first()
    if request.method == GET:
        return u.profile()
    if request.method == PATCH:
        form = json.loads(request.data)
        u.email = form["email"]
        u.incie = form["incie"]
        u.salcie = form["salcie"]
        u.mucie = form["mucie"]
        db.session.commit()
        return "Changes to profile saved."


@bp.route('/password/<int:user_id>', methods=[PATCH])
@login_required
def password(user_id):
    u = User.query.filter(User.user_id == user_id).first()
    form = json.loads(request.data)
    if u.check_password(form["current"]):
        if form["password1"] == form["password2"]:
            u.set_password(form["password1"], increment=False)
            db.session.commit()
            return "Password changed."
        return json_error("Passwords are not equal.")
    return json_error("Incorrect password.")


@bp.route('/logout', methods=[POST])
@login_required
def logout():
    return jsonify("Logged out")


@bp.route('/test', methods=[GET])
@login_required
def renew():
    return jsonify(current_user.profile())
