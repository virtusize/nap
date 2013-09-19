# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy.types import Integer, Unicode

from nap.validators import FieldValidator, EnsureNotNone
from sa_nap.model import Field, SAModelSerializer
from sa_nap.validators import SQLConstraintsValidator

from tests.fixtures import Users, User, Store, Stores, StoreMemberships, StoreMembership, fixture_loader

from nap.exceptions import ModelInvalidException
from nap.validation import ValidationResult
from tests.helpers import *


def test_fixtures_query():

    with db(), fixtures(Users, fixture_loader=fixture_loader):
        john = db_session.query(User).get(Users.john.id)
        assert_is_not_none(john)


def test_validate_invalid():
    john = User(name='Invalid John')
    assert_false(john.validate())


def _assert_sql_constraints_validator(field, value, expected):
    validator = SQLConstraintsValidator(field)
    result = ValidationResult(validator.validate(None, 'test_field', value))
    assert_equals(bool(result), expected)


def test_sql_constraints_validator():
    cases = [
        (Field(sa.String, primary_key=True), None, True),
        (Field(sa.String, primary_key=True), False, True),
        (Field(sa.Unicode(10)), u'', True),
        (Field(sa.Unicode(10)), '', False),
        (Field(sa.UnicodeText), u'', True),
        (Field(sa.UnicodeText), '', False),
        (Field(sa.UnicodeText(10)), u'_' * 11, False),
        (Field(sa.UnicodeText(10)), '', False),
        (Field(sa.Integer, nullable=False), None, False),
        (Field(sa.Integer, nullable=False), 0, True),
        (Field(sa.Integer, nullable=False), 1, True),
    ]

    for case in cases:
        yield (_assert_sql_constraints_validator,) + case


@raises(ModelInvalidException)
def test_validate_before_insert():
    with db():
        user = User(name='Hannes')
        db_session.add(user)
        db_session.commit()


@raises(ModelInvalidException)
def test_validate_before_insert():
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        john = db_session.query(User).get(Users.john.id)
        john.email = None
        db_session.commit()


def test_to_dict():
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        john = db_session.query(User).get(Users.john.id)

        compare(SAModelSerializer().serialize(john), {'name': 'John', 'email': 'john@virtusize.com', 'id': 1, 'password': '123456'})


def test_tablename():
    assert_equal(Store.__tablename__, 'stores')
    assert_equal(User.__tablename__, 'users')


def test_column():

    class SomeModel(SAModel):
        id = sa.Column(sa.Integer, primary_key=True)
        some_column = sa.Column(sa.String(255))

    sm = SomeModel(some_column='some_value')
    assert_is_not_none(sm)
    assert_equal(sm.some_column, 'some_value')


def test_validate_with():

    class AnotherModel(SAModel):
        id = sa.Column(sa.Integer, primary_key=True)
        some_column = sa.Column(sa.String(255))

        _validate_with = [FieldValidator('some_column', EnsureNotNone)]

    sm = AnotherModel(some_column='some_value')
    assert_is_not_none(sm.some_column)
    assert_true(sm.validate())

    sm = AnotherModel()
    assert_is_none(sm.some_column)
    assert_false(sm.validate())
    assert_equal(len(sm.validate().errors), 1)


def test_multiple_models_on_same_table():
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.schema import Column

    Base = declarative_base()

    class LegacyUser(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(Unicode(255))
        email = Column(Unicode(255))
        password = Column(Unicode(255))

    with db(), fixtures(Users, fixture_loader=fixture_loader):
        john = db_session.query(User).get(Users.john.id)
        legacy_john = db_session.query(LegacyUser).get(Users.john.id)

        assert_is_not_none(john)
        assert_is_not_none(legacy_john)

        john_dct = john.__dict__
        legacy_john_dct = john.__dict__
        del legacy_john_dct['_sa_instance_state']

        compare(john_dct, legacy_john_dct)


def test_model_associations_with_compound_private_key():
    with db(), fixtures(Users, Stores, StoreMemberships, fixture_loader=fixture_loader):
        john = db_session.query(User).get(Users.john.id)
        johns_memberships = db_session.query(StoreMembership).filter(StoreMembership.user_id==Users.john.id).all()

        compare(john.store_memberships, johns_memberships)

        virtusize = db_session.query(Store).get(Stores.virtusize.id)
        assert_equal(len(virtusize.store_memberships), 2)


def test_model_with_custom_tablename():

    class LegacyTableModel(SAModel):
        __tablename__ = 'old_style_tablename'
        id = Field(Integer, primary_key=True)

    assert_equal(LegacyTableModel.__tablename__, 'old_style_tablename')
