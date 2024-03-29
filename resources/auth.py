from flask import request
from flask_restful import Resource

from managers.auth import AuthManager
from schemas.request_schema.users import (
    UserRegistrationRequestSchema,
    UserLoginRequestSchema,
)
from schemas.response_schema.users import UserAuthResponseSchema
from utils.decorators import validate_schema


class RegisterResource(Resource):
    @validate_schema(UserRegistrationRequestSchema)
    def post(self):
        data = request.get_json()
        user = AuthManager.create_user(data)
        token = AuthManager.encode_token(user)
        return UserAuthResponseSchema().dump({"token": token})


class LoginResource(Resource):
    @validate_schema(UserLoginRequestSchema)
    def post(self):
        data = request.get_json()
        user = AuthManager.login_user(data)
        token = AuthManager.encode_token(user)
        return UserAuthResponseSchema().dump({"token": token})
