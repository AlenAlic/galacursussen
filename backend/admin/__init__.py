from flask import Blueprint

bp = Blueprint('admin', __name__)

from backend.admin import routes
