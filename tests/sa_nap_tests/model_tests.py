# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.exc import IntegrityError

from nap.validators import FieldValidator, EnsureNotNone
from sa_nap.model import Field, SAModelSerializer, NoSessionBound, ModelJSON
from sa_nap.validators import SQLConstraintsValidator

from tests.fixtures import Users, User, Store, Stores, StoreMemberships, StoreMembership, Product, ProductTypes, ProductType, Products, ProductTypeDBModel, fixture_loader

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
        (Field(sa.Integer, nullable=False, default=0), None, True),
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
def test_validate_before_update():
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


def test_unique_validator():
    with db():
        user1 = User(name=u'Joe', email='valid@example.com', password='12345')
        user2 = User(name=u'Jan', email='valid@example.com', password='12345')

        assert_true(user1.validate())
        assert_true(user2.validate())

        db_session.add(user1)
        assert_true(user1.validate())
        assert_false(user2.validate())

        db_session.delete(user1)
        assert_true(user2.validate())


@raises(ModelInvalidException)
def test_unique_validator_without_constraint_and_multiple_models_already_in_db():
    with db():
        product1 = Product(name=u'Garment', store_id=Stores.virtusize.id, product_type_id=ProductTypes.shirt.id)
        product2 = Product(name=u'Garment', store_id=Stores.virtusize.id, product_type_id=ProductTypes.shirt.id)
        db_session.add(product1)
        db_session.add(product2)
        db_session.commit()

        product3 = Product(name=u'Garment', store_id=Stores.virtusize.id, product_type_id=ProductTypes.shirt.id)
        db_session.add(product3)
        db_session.commit()


@raises(ModelInvalidException)
def test_unique_validator_without_constraint_and_multiple_models_already_in_db():
    with db():
        product1 = Product(name=u'Garment', store_id=Stores.virtusize.id, product_type_id=ProductTypes.shirt.id)
        product2 = Product(name=u'Garment', store_id=Stores.virtusize.id, product_type_id=ProductTypes.shirt.id)
        db_session.add(product1)
        db_session.add(product2)
        db_session.commit()

        product3 = Product(name=u'Garment', store_id=Stores.virtusize.id, product_type_id=ProductTypes.shirt.id)
        db_session.add(product3)
        db_session.commit()


@raises(ModelInvalidException)
def test_unique_validator_by_db_insert():
    with db():
        user1 = User(name=u'Joe', email='valid@example.com', password='12345')
        user2 = User(name=u'Jan', email='valid@example.com', password='12345')

        db_session.add(user1)
        db_session.commit()

        db_session.add(user2)
        db_session.commit()


@raises(IntegrityError)
def test_unique_validator_by_db_insert_same_commit():
    with db():
        user1 = User(name=u'Joe', email='valid@example.com', password='12345')
        user2 = User(name=u'Jan', email='valid@example.com', password='12345')

        db_session.add(user1)
        db_session.add(user2)
        db_session.commit()


def test_samodel_to_model_relation():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        p = db_session.query(Product).get(Products.dress.id)
        compare(p.product_type, ProductTypes.dress)


def test_model_json_type_decorator():
    mj = ModelJSON(ProductType)
    dog_collar = ProductType(id=123, name=u'Dog cöllår', awesome=True)

    serialized = mj.process_bind_param(dog_collar, None)
    compare(serialized, '{"awesome": true, "name": "Dog c\\u00f6ll\\u00e5r", "id": 123}')

    deserialized = mj.process_result_value(serialized, None)
    assert_is_instance(deserialized, ProductType)
    compare(deserialized, dog_collar)
    assert_equal(deserialized.name, u'Dog cöllår')
    assert_equal(deserialized.awesome, True)


def test_samodel_model_serialized():
    with db():
        dress = ProductTypes.dress
        pt = ProductTypeDBModel()
        pt.product_type = dress
        db_session.add(pt)
        db_session.commit()

        db_session.refresh(pt)
        compare(pt.product_type, dress)

        pt.product_type = ProductTypes.shirt
        db_session.commit()

        db_session.refresh(pt)
        compare(pt.product_type, ProductTypes.shirt)


def test_samodel_model_serialized_mutable():
    with db():
        mutable_type = ProductType(id=100, name=u'Version 1')
        pt = ProductTypeDBModel()
        pt.product_type = mutable_type
        db_session.add(pt)
        db_session.commit()

        db_session.refresh(pt)
        compare(pt.product_type, mutable_type)

        pt.product_type.name = u'Version 2'

        assert_equal(pt.product_type.name, u'Version 2')
        db_session.commit()

        db_session.refresh(pt)
        assert_equal(pt.product_type.name, u'Version 2')


@raises(ModelInvalidException)
def test_samodel_model_serialized_mutable_validation():
    with db():
        mutable_type = ProductType(id=100)
        assert_false(mutable_type.validate())

        pt = ProductTypeDBModel()
        pt.product_type = mutable_type
        db_session.add(pt)
        db_session.commit()


@raises(NoSessionBound)
def test_missing_db_session():
    class MissingDBSessionModel(SAModel):
        id = Field(Integer, primary_key=True, autoincrement=True)
        __db_session__ = None

    assert_is_none(MissingDBSessionModel.__db_session__)
    MissingDBSessionModel.get_session()
