from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth import auth
from models import TransactionModel


def validate_schema(schema_name):
    def decorated_func(func):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            schema = schema_name()
            errors = schema.validate(data)
            if not errors:
                return func(*args, **kwargs)
            raise BadRequest(errors)

        return wrapper

    return decorated_func


def permission_required(permission_role):
    def decorated_func(func):
        def wrapper(*args, **kwargs):
            current_user = auth.current_user()
            if current_user.role == permission_role:
                return func(*args, **kwargs)
            raise Forbidden("You not have permission to access this")

        return wrapper

    return decorated_func


def validate_complaint_id(complaint_id):
    def decorated_func(func):
        def wrapper(*args, **kwargs):
            complaint = TransactionModel.query.filter_by(complaint_id=complaint_id).first()
            if not complaint:
                raise BadRequest("Complaint does not exist")
            return func(*args, **kwargs)

        return wrapper

    return decorated_func
