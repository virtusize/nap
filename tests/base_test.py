# -*- coding: utf-8 -*-

from helpers import *
from fixtures import *


def test_fixtures_query():

    with db(), fixtures(Users):
        john = db_session.query(User).get(Users.john.id)
        assert_is_not_none(john)


def test_validate_invalid():

    with db(), fixtures(Users):
        john = db_session.query(User).get(Users.invalid_john.id)
        assert_false(john.validate())
