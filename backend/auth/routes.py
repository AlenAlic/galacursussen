from flask import jsonify
from flask_login import login_user, logout_user, current_user, login_required
from backend import db
from backend.auth import bp
from backend.auth.forms import LoginForm
from backend.models import User
from backend.auth.email import send_password_reset_email
from backend.responses import json_unauthorized
from backend.values import *


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


@bp.route('/user/<int:user_id>', methods=[GET])
def user(user_id):
    u = User.query.filter(User.user_id == user_id).first()
    return u.profile()


@bp.route('/logout', methods=[POST])
@login_required
def logout():
    return jsonify("Logged out")


@bp.route('/test', methods=[GET])
@login_required
def renew():
    return jsonify(current_user.profile())


# @bp.route('/reset_password_request', methods=['GET', 'POST'])
# def reset_password_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     form = ResetPasswordRequestForm()
#     if request.method == "POST":
#         if form.validate_on_submit():
#             user = User.query.filter(User.email==form.email.data).first()
#             if user is not None:
#                 send_password_reset_email(user)
#                 flash('Check your email for the instructions to reset your password.')
#             else:
#                 flash("This e-mail address is not registered here.")
#             return redirect(url_for('main.index'))
#     return render_template('auth/reset_password_request.html', title='Reset Password', form=form)
#
#
# @bp.route('/reset_password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     user = User.verify_reset_password_token(token)
#     if not user:
#         return redirect(url_for('main.index'))
#     if user == 'error':
#         flash('Not a valid token.', 'danger')
#         return redirect(url_for('main.index'))
#     form = ResetPasswordForm()
#     if request.method == "POST":
#         if form.validate_on_submit():
#             user.set_password(form.password.data)
#             db.session.commit()
#             flash('Your password has been reset.', 'success')
#             return redirect(url_for('main.index'))
#     return render_template('auth/reset_password.html', form=form, user=user)
#
#
# @bp.route('/activate_account/<token>', methods=['GET', 'POST'])
# def activate_account(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#     user = User.verify_reset_password_token(token)
#     if not user:
#         return redirect(url_for('main.index'))
#     if user == 'error':
#         flash('Not a valid token.', 'danger')
#         return redirect(url_for('main.index'))
#     form = ResetPasswordForm()
#     form.submit.label.text = "Set password"
#     if request.method == "POST":
#         if form.validate_on_submit():
#             user.set_password(form.password.data)
#             db.session.commit()
#             flash('Your password has been set.', 'success')
#             return redirect(url_for('main.login'))
#     return render_template('auth/activate_account.html', form=form, user=user)
