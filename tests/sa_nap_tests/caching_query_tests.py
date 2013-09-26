# -*- coding: utf-8 -*-
from dogpile.cache import make_region

from sqlalchemy import event
from sa_nap.caching_query import CachingQuery, using_cache, _key_from_query

from tests.fixtures import Users, User, fixture_loader
from tests.helpers import *


#This is important ad we use a custom query impl.
db_session = scoped_session(sessionmaker(bind=engine, query_cls=CachingQuery))

query_count = 0

#A simple in memory cache with 60 sec timeout
memory_cache = make_region().configure('dogpile.cache.memory', expiration_time=60)

@event.listens_for(engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    global query_count
    query_count += 1


def test_query_count():
    """
    Test test if the query count counts up as expected.
    """
    with db():
        global query_count
        query_count = 0

        db_session.query(User).get(Users.john.id)
        compare(query_count, 1)

        db_session.query(User).get(Users.john.id)
        compare(query_count, 2)

        db_session.query(User).get(Users.jane.id)
        compare(query_count, 3)


def test_caching_query_on_simple_get():
    """
    This is not entierly complete.
    In order for the invalidation to work, the query must not be executed.
    So using first() all() count() etc... will execute the query.
    So invalidation wont work with those.

    all() and one() are the only calls that do not modify the query and
    thus can be used with invalidate()
    """

    with db(), fixtures(Users, fixture_loader=fixture_loader):
        global query_count
        query_count = 0

        john_query = db_session.\
            query(User).\
            options(using_cache(memory_cache)).\
            filter(User.name == Users.john.name)

        jane_query = db_session. \
            query(User). \
            options(using_cache(memory_cache)). \
            filter(User.name == Users.jane.name)

        print _key_from_query(john_query)
        print _key_from_query(jane_query)

        john_query.one()
        compare(query_count, 1)

        john_query.one()
        compare(query_count, 1)

        jane_query.one()
        compare(query_count, 2)

        jane_query.one()
        compare(query_count, 2)

        john_query.invalidate()
        john_query.one()
        compare(query_count, 3)
