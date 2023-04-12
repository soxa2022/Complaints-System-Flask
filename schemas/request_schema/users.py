from marshmallow import fields

from schemas.base import UserRequestBaseSchema


class UserRegistrationRequestSchema(UserRequestBaseSchema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone = fields.String(required=True)
    # We made it with 'metadata',because we received testing warnings
    iban = fields.String(
        metadata={"min_length": 22, "max_length": 22, "Required": True}
    )


class UserLoginRequestSchema(UserRequestBaseSchema):
    pass
