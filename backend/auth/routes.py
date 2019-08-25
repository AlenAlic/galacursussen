from flask import jsonify, request, json, render_template, current_app
from flask_login import login_required
from backend.auth import bp
from backend.auth.forms import LoginForm
from backend.models import User
from backend.responses import json_unauthorized, json_error
from backend.values import *
from backend import db
from backend.util import auth_token
from backend.email import send_email


@bp.route('/login', methods=[POST])
def login():
    form = LoginForm()
    if form.validate():
        u = User.query.filter(User.email.ilike(form.email.data)).first()
        if u is None or not u.check_password(form.password.data):
            return json_unauthorized("Invalid username or password")
        elif u.is_active:
            return jsonify(u.get_auth_token(expires_in=31536000 if form.remember_me.data else 86400))
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
        u.first_name = form["first_name"]
        u.last_name = form["last_name"]
        u.email = form["email"]
        u.incie = form["incie"]
        u.salcie = form["salcie"]
        u.mucie = form["mucie"]
        db.session.commit()
        return OK


@bp.route('/password/<int:user_id>', methods=[PATCH])
@login_required
def password(user_id):
    u = User.query.filter(User.user_id == user_id).first()
    form = json.loads(request.data)
    if u.check_password(form["current"]):
        if form["password1"] == form["password2"]:
            u.set_password(form["password1"], increment=False)
            db.session.commit()
            return OK
        return json_error("Passwords are not equal.")
    return json_error("Incorrect password.")


@bp.route('/logout', methods=[POST])
@login_required
def logout():
    return jsonify("Logged out")


def send_account_activation_email(u):
    send_email(f"Account activation {current_app.config['PRETTY_URL']}.",
               recipients=[u.email],
               text_body=render_template('email/activate_account.txt', user=u),
               html_body=render_template('email/activate_account.html', user=u))


@bp.route('/create', methods=[POST])
@login_required
def create():
    form = json.loads(request.data)
    u = User()
    u.first_name = form["first_name"]
    u.last_name = form["last_name"]
    u.email = form["email"]
    u.incie = form["incie"]
    u.salcie = form["salcie"]
    u.mucie = form["mucie"]
    u.access = form["account"]
    u.auth_code = auth_token()
    db.session.add(u)
    db.session.commit()
    send_account_activation_email(u)
    return jsonify(u.created())


@bp.route('/activate/<string:token>', methods=[GET])
def activate(token):
    u = User.query.filter(User.auth_code == token).first()
    if u is not None:
        return jsonify(u.get_reset_password_token())
    else:
        return json_error("Invalid token")


@bp.route('/password/set/<string:token>', methods=[PATCH])
def set_password(token):
    u = User.verify_reset_password_token(token)
    if u != "error":
        form = json.loads(request.data)
        if form["password1"] == form["password2"]:
            u.set_password(form["password1"])
            u.auth_code = None
            u.is_active = True
            db.session.commit()
            return OK
        return json_error("Passwords are not equal.")
    return json_error("Token is invalid")


def send_password_reset_email(u):
    token = u.get_reset_password_token(expires_in=3600)
    send_email(f"Password reset {current_app.config['PRETTY_URL']}.",
               recipients=[u.email],
               text_body=render_template('email/reset_password.txt', user=u, token=token),
               html_body=render_template('email/reset_password.html', user=u, token=token))


@bp.route('/password/reset', methods=[POST], defaults={"token": None})
@bp.route('/password/reset/<string:token>', methods=[PATCH])
def reset_password(token):
    if request.method == POST:
        data = json.loads(request.data)
        u = User.query.filter(User.email.ilike(data["email"])).first()
        if u is not None:
            send_password_reset_email(u)
        return OK
    if request.method == PATCH:
        u = User.verify_reset_password_token(token)
        if u != "error":
            if not u.is_active:
                return json_error("Cannot reset the password of an account that has not been activated.")
            form = json.loads(request.data)
            if form["password1"] == form["password2"]:
                u.set_password(form["password1"])
                u.auth_code = None
                u.is_active = True
                db.session.commit()
                return OK
            return json_error("Passwords are not equal.")
        return json_error("Token is invalid")


@bp.route('/renew', methods=[GET])
@login_required
def renew():
    return "Renew"


@bp.route('/test', methods=[GET])
def test():
    return render_template("test.html")
