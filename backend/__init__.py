from flask import Flask, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, AnonymousUserMixin, current_user
from flask_mail import Mail
from backend.values import *
from datetime import datetime


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
mail = Mail()


class Anonymous(AnonymousUserMixin):

    @staticmethod
    def is_admin():
        return False

    @staticmethod
    def is_organizer():
        return False

    @staticmethod
    def is_member():
        return False

    @staticmethod
    def is_treasurer():
        return False

    @staticmethod
    def profile():
        return None


def create_app():
    from backend.models import User, Course
    from backend.tests.data import test_users, test_courses
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.url_map.strict_slashes = False

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:'))
    login.init_app(app)
    login.anonymous_user = Anonymous
    mail.init_app(app)

    @app.before_request
    def before_request_callback():
        g.values = values
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.session.commit()

    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT, PATCH'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    app.after_request(add_cors_headers)

    @app.context_processor
    def inject_now():
        return {'now': f"?{int(datetime.utcnow().timestamp())}"}

    @app.shell_context_processor
    def make_shell_context():
        return {
            'create_admin': create_admin,
            'create_test_users': create_test_users,
            'create_test_courses': create_test_courses
        }

    def create_admin(email, password, first_name, last_name, incie=False, salcie=False, mucie=False):
        if len(User.query.filter(User.access == values.ACCESS[values.ADMIN]).all()) == 0:
            a = User()
            a.email = email
            a.set_password(password)
            a.access = values.ACCESS[values.ADMIN]
            a.is_active = True
            a.first_name = first_name
            a.last_name = last_name
            a.incie = incie
            a.salcie = salcie
            a.mucie = mucie
            db.session.add(a)
            db.session.commit()

    def create_test_users():
        if len(User.query.all()) == 0:
            test_users()

    def create_test_courses():
        if len(Course.query.all()) == 0:
            test_courses()

    from backend.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from backend.courses import bp as courses_bp
    app.register_blueprint(courses_bp, url_prefix='/courses')

    return app


# noinspection PyPep8
from backend import models
