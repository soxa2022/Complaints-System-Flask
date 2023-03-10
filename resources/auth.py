from flask import request
from flask_restful import Resource

from app import db
from models import User
from schemas.request_schema.user import UserRegistrationRequestSchema
from utils.decorators import validate_schema


class RegisterResource(Resource):
    @validate_schema(UserRegistrationRequestSchema)
    def post(self):
        data = request.get_json()
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return {"massage": "ok"}
