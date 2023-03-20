from marshmallow import fields, Schema


class UserRequestBaseSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class UserResponseBaseSchema(Schema):
    email = fields.Email(required=True)
