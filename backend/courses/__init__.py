from flask import Blueprint

bp = Blueprint('courses', __name__)

from backend.courses import routes
