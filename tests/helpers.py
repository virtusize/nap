# -*- coding: utf-8 -*-

"""
BaseTestCase sets up the basic test environment

The TestCases can but don't have to inherit from this class.
If the tests do not need a full test environment incl. the database they can be
regular unittest.TestCases
"""

import testfixtures
from nose import tools as nt

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from sa_nap import SAModel


assert_equal = nt.assert_equal
assert_equals = nt.assert_equals
assert_not_equal = nt.assert_not_equal
assert_true = nt.assert_true
assert_false = nt.assert_false
assert_is = nt.assert_is
assert_is_not = nt.assert_is_not
assert_is_none = nt.assert_is_none
assert_is_not_none = nt.assert_is_not_none
assert_in = nt.assert_in
assert_not_in = nt.assert_not_in
assert_is_instance = nt.assert_is_instance
assert_not_is_instance = nt.assert_not_is_instance
assert_almost_equal = nt.assert_almost_equal
assert_not_almost_equal = nt.assert_not_almost_equal
assert_greater = nt.assert_greater
assert_greater_equal = nt.assert_greater_equal
assert_less = nt.assert_less
assert_less_equal = nt.assert_less_equal
assert_list_equal = nt.assert_list_equal
assert_tuple_equal = nt.assert_tuple_equal
assert_set_equal = nt.assert_set_equal
assert_dict_equal = nt.assert_dict_equal
compare = testfixtures.compare
raises = nt.raises


engine = create_engine('sqlite:///:memory:', echo=True)


db_session = scoped_session(sessionmaker(bind=engine))


def fixtures(*args, **kwargs):
    return FixturesContext(*args, **kwargs)


def db(clean=True):
    return DbContext(clean=clean)


class DbContext(object):
    """
    Sets up a clean db context by populating the
    in-memory sqlite db with tables.
    At tear down, all tables are dropped (unless drop_tables is False)
    and the session is removed (A new one will be created next time 'db_session' is referenced.)
    """

    def __init__(self, clean):
        self._clean = clean

    def __enter__(self):
        if self._clean:
            SAModel.metadata.drop_all(engine)

        SAModel.metadata.create_all(engine)

    def __exit__(self, type, value, traceback):
        db_session.remove()


class FixturesContext(object):
    """
    Populates the db with all fixtures.
    """
    def __init__(self, *args, **kwargs):
        fixture_loader = kwargs.pop('fixture_loader')
        self.fixture_list = args
        self.data = fixture_loader.data(*self.fixture_list)

    def __enter__(self):
        self.data.setup()

    def __exit__(self, type, value, traceback):
        self.data.teardown()
