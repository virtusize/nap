# -*- coding: utf-8 -*-

from core.validation import ValidationResult
import sqlalchemy as sa
from tests.helpers import *
from tests.core_tests.database_fixtures import Users, User, Store, fixture_loader


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


@raises(ValueError)
def test_validate_before_insert():
    with db():
        user = User(name='Hannes')
        db_session.add(user)
        db_session.commit()


@raises(ValueError)
def test_validate_before_insert():
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        john = db_session.query(User).get(Users.john.id)
        john.email = None
        db_session.commit()


def test_to_dict():
    john = User(name='John Doe', email='john@doe.com')
    dct = john.to_dict()
    del dct['_sa_instance_state']
    assert_equal(dct, {'name': 'John Doe', 'email': 'john@doe.com'})


def test_tablename():
    assert_equal(Store.__tablename__, 'stores')
    assert_equal(User.__tablename__, 'users')


def test_controller():
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        c = SAModelController(User, db_session)
        user = c.read(1)
        assert_is_not_none(user)

        email = 'somebody@example.com'
        c.update(user.id, {'email': email})

        user = c.read(1)
        compare(user.email, email)

        user = c.create({'name': u'Anybody', 'email': 'anybody@example.com'})
        assert_is_not_none(user)
        compare(c.read(user.id), user)
        compare(user.name, 'Anybody')

        c.delete(user.id)
        assert_is_none(c.read(user.id))
