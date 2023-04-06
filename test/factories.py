from datetime import datetime
import random

import factory

from db import db
from models import User, RoleType, State, Complaint


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        obj = super().create(**kwargs)
        db.session.add(obj)
        db.session.flush()
        return obj


class UserFactory(BaseFactory):
    class Meta:
        model = User
    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = str(random.randint(1000000, 2000000))
    password = factory.Faker("password")
    role = RoleType.complainer
    iban = factory.Faker("iban")
    is_deleted = False


# class ComplaintFactory(BaseFactory):
#     class Meta:
#         model = Complaint
#     id = factory.Sequence(lambda n: n)
#     title = factory.Faker("title")
#     description = factory.Faker("description")
#     photo_url = factory.Faker("photo_url")
#     amount = random.randint(100, 200)
#     created_at = datetime.utcnow()
#     status = State.pending
#     user_id = 1
#     is_deleted = False
