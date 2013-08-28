# -*- coding: utf-8 -*-

from helpers import *
from tests.core_database_fixtures import Users, User, fixture_loader


def test_fixtures_query():

    with db(), fixtures(Users, fixture_loader=fixture_loader):
        john = db_session.query(User).get(Users.john.id)
        assert_is_not_none(john)


def test_validate_invalid():

    with db(), fixtures(Users, fixture_loader=fixture_loader):
        john = db_session.query(User).get(Users.invalid_john.id)
        assert_false(john.validate())