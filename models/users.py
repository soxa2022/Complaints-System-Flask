from db import db
from models.enum import RoleType


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Enum(RoleType), default=RoleType.complainer, nullable=False)
    iban = db.Column(db.String(22))
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)
