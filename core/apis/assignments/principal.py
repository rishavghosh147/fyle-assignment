from flask import Blueprint
from core.apis import decorators
from core.models.assignments import Assignment
from .schema import AssignmentSchema,AssignmentGradeSchema
from core.apis.responses import APIResponse
from core import db

principal_assignments_resources=Blueprint('principal_assignments_resources',__name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def get_all_submited_or_graded_assignments(p):
    assignments=Assignment.get_assignment_submited_or_graded()
    students_assignments_dump=AssignmentSchema().dump(assignments)
    return APIResponse.respond(data=students_assignments_dump)


@principal_assignments_resources.route('/assignments/grade',methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_or_regrade_a_submitted_assignment(p, incoming_payload):
    grade_assignment_payload=AssignmentGradeSchema().load(incoming_payload)

    graded_assignment=Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump=AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)