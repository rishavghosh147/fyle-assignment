from flask import jsonify, request
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources
from core.apis.teachers import principal_teachers_resources
from core.apis.assignments import principal_assignments_resources
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException

from sqlalchemy.exc import IntegrityError

app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal_teachers_resources, url_prefix='/principal')
app.register_blueprint(principal_assignments_resources, url_prefix='/principal')


@app.route('/')
def ready():
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })

    return response


@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        all_apis = ['/student/assignments', '/student/assignments/submit', '/teacher/assignments', '/teacher/assignments/grade', '/principal/assignments', '/principal/teachers', '/principal/assignments/grade']
        if request.path not in all_apis:
            fyle_error = FyleError(status_code=404, message='No such API')
            return jsonify(fyle_error.to_dict()), 404
        else:
            return jsonify(error=err.__class__.__name__, message=str(err)), err.code

    return jsonify(error=err.__class__.__name__, message=str(err)), 500
    # raise err
