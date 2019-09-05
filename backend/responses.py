from flask import jsonify
from backend.values import ERRORS


def json_error(errors, status=400):
    errors = [errors] if isinstance(errors, str) else errors
    return jsonify({ERRORS: errors}), status


def json_unauthorized(errors):
    return json_error(errors, 401)


def json_forbidden(errors):
    return json_error(errors, 403)


def no_content():
    return "", 204
