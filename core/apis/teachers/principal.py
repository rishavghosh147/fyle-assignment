from flask import Blueprint
from core.apis import decorators
from core.models.teachers import Teacher
from .schema import TeacherSchema
from core.apis.responses import APIResponse

principal_teachers_resources = Blueprint('principal_teachers_resources', __name__)

@principal_teachers_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def All_teachers(p):
    """Return list of all teachers"""
    teachers=Teacher.get_all()
    data=TeacherSchema().dump(teachers)
    return APIResponse.respond(data=data)
