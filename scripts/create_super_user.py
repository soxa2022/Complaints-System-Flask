from werkzeug.security import generate_password_hash

from db import db
from models import User, RoleType


def create_super_user(first_name, last_name, email, phone, password):
    password_hash = generate_password_hash(password)
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        role=RoleType.admin,
        password=password_hash,
    )
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    create_super_user()
