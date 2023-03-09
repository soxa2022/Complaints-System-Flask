from marshmallow import Schema, fields


class UserRegistrationRequestSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    phone = fields.String(required=True)
    iban = fields.String(required=True)
    is_deleted = fields.Boolean(required=True)

