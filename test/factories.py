import factory

from db import db
from models import User, RoleType, State, Complaint, TransactionModel
from test.base import mock_uuid


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
    phone = str(factory.Faker("random_number", digits=8))
    password = factory.Faker("password")
    role = RoleType.complainer
    iban = factory.Faker("iban")
    is_deleted = False


def get_user_id():
    return UserFactory().id


class ComplaintFactory(BaseFactory):
    class Meta:
        model = Complaint

    id = factory.Sequence(lambda n: n)
    title = factory.Faker("word")
    description = factory.Faker("sentence")
    photo_url = factory.Faker("url")
    amount = factory.Faker("pyfloat")
    created_at = factory.Faker("date_time")
    status = State.pending
    user_id = factory.LazyFunction(get_user_id)
    is_deleted = False


def get_complaint_id():
    return ComplaintFactory().id


class TransactionFactory(BaseFactory):
    class Meta:
        model = TransactionModel

    id = factory.Sequence(lambda n: n)
    quote_id = mock_uuid()
    transfer_id = mock_uuid()
    custom_transfer_id = mock_uuid()
    target_account_id = mock_uuid()
    amount = factory.Faker("pyfloat")
    create_at = factory.Faker("date_time")
    complaint_id = factory.LazyFunction(get_complaint_id)
