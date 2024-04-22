from marshmallow import Schema, EXCLUDE, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from core.models.teachers import Teacher

class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE

    id = auto_field(required=True, allow_none=False)
    user_id = auto_field(required=True, allow_none=False)
    created_at = auto_field(dump_only=True)
    updated_at = auto_field(dump_only=True)
