from marshmallow import fields

from schemas.base import ComplaintBaseSchema


class ComplaintRequestSchema(ComplaintBaseSchema):
    photo = fields.Str(Required=True)
    extension = fields.String(required=True)
