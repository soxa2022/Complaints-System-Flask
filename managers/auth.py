from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import DecodeError
from werkzeug.exceptions import BadRequest, Unauthorized
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models.users import User


class AuthManager:
    @staticmethod
    def create_user(user_data):
        user = User.query.filter_by(email=user_data["email"]).first()
        if not user:
            user_data["password"] = generate_password_hash(user_data["password"])
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()
            return user
        raise BadRequest("The email already exists")

    @staticmethod
    def login_user(user_data):
        user = User.query.filter_by(email=user_data["email"]).first()
        if not user:
            raise BadRequest("Invalid email or password")
        if not check_password_hash(user.password, user_data["password"]):
            raise BadRequest("Invalid email or password")
        return user

    @staticmethod
    def encode_token(user):
        payload = {"sub": user.id, "exp": datetime.utcnow() + timedelta(days=2)}
        return jwt.encode(payload, config("JWT_KEY"), "HS256")

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, key=config("JWT_KEY"), algorithms=["HS256"])
        except DecodeError as ex:
            raise BadRequest("Invalid or missing token")


auth = HTTPTokenAuth(scheme="Bearer")


# @auth.verify_token(token):
#
#
# try:
#     payload = AuthManager.decode_token(token)
#     user = User.query.filter_by(id=payload["sub"]).first()
#     if not user:
#         raise Unauthorized("Invalid or missing user")
#     return user
# except Exception as ex:
#     raise Unauthorized("Invalid or missing token")
