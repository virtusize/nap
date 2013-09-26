# -*- coding: utf-8 -*-


import sqlalchemy as sa

from tests.fixtures import Users, User, fixture_loader
from tests.helpers import *


def test_pickling_a_model_instance():
    """
    Test the detached state of a pickled model instance.
    And modifying an detached object wont modify the DB row.

    """
    import cPickle as pickle
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        user_1 = db_session.query(User).get(Users.john.id)
        assert_false(sa.inspect(user_1).detached)

        user_bytes = pickle.dumps(user_1, pickle.HIGHEST_PROTOCOL)
        user_2 = pickle.loads(user_bytes)
        assert_true(sa.inspect(user_2).detached)

        user_2.name = u'Johnny'
        db_session.commit()

        user_3 = db_session.query(User).get(Users.john.id)
        assert_not_equal(user_2.name, user_3.name)


def test_modifying_a_pickled_instance():
    """
    Same as above, but this time
    the data is merged back into session without performing
    a db load, this way we can modify the pickled instance
    and this will modify the row.
    """
    import cPickle as pickle
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        user_1 = db_session.query(User).get(Users.john.id)

        user_bytes = pickle.dumps(user_1, pickle.HIGHEST_PROTOCOL)
        user_2 = pickle.loads(user_bytes)
        user_2 = db_session.merge(user_2, load=False)

        assert_false(sa.inspect(user_2).detached)

        user_2.name = u'Johnny'
        db_session.commit()

        user_3 = db_session.query(User).get(Users.john.id)
        compare(user_2.name, user_3.name)


def test_modifying_a_pickled_instance_that_has_changed():
    """
    Same as above, but this time
    modify the underlying instance and see that the value is stale,
    but a commit wont commit the stale value.
    Only the modified value. (in this case email)
    """
    import cPickle as pickle
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        user_1 = db_session.query(User).get(Users.john.id)

        user_bytes = pickle.dumps(user_1, pickle.HIGHEST_PROTOCOL)

        user_1.name = u'Sammy'
        db_session.commit()

        user_2 = pickle.loads(user_bytes)
        user_2 = db_session.merge(user_2, load=False)

        assert_false(sa.inspect(user_2).detached)

        #The name is still John here. so the pickled version is stale.
        compare(user_2.name, u'John')

        user_2.email = 'email@example.com'
        db_session.commit()

        user_3 = db_session.query(User).get(Users.john.id)

        #But sqlalhemy does the right thing at only modifies the email
        compare(user_2.name, user_3.name)
        compare(u'Sammy', user_3.name)
        compare('email@example.com', user_3.email)
