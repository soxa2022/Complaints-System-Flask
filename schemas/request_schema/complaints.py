from marshmallow import fields

from schemas.base import ComplaintBaseSchema


class ComplaintRequestSchema(ComplaintBaseSchema):
    photo = fields.Str(metadata={"Required": True})
    extension = fields.String(metadata={"Required": True})
