from marshmallow import fields, Schema


class UserRequestBaseSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    is_deleted = fields.Boolean()


class UserResponseBaseSchema(Schema):
    email = fields.Email(required=True)


class ComplaintBaseSchema(Schema):
    title = fields.Str(Required=True)
    description = fields.Str(Required=True)
    amount = fields.Float(Required=True)
    is_deleted = fields.Boolean()