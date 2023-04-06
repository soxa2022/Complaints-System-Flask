from marshmallow import fields

from schemas.base import UserRequestBaseSchema


class UserRegistrationRequestSchema(UserRequestBaseSchema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone = fields.String(required=True)
    iban = fields.String(min_length=22, max_length=22, required=True)


class UserLoginRequestSchema(UserRequestBaseSchema):
    pass
