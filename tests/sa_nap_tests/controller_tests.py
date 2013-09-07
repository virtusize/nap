# -*- coding: utf-8 -*-
from sa_nap.controller import SAModelController
from tests.fixtures import Users, fixture_loader, User
from tests.helpers import db, fixtures, db_session, assert_is_not_none, compare, assert_is_none


def test_controller():
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        c = SAModelController(User, db_session)
        user = c.read(1)
        assert_is_not_none(user)

        email = 'somebody@example.com'
        c.update(user.id, {'email': email})

        user = c.read(1)
        compare(user.email, email)

        user = c.create({'name': u'Anybody', 'email': 'anybody@example.com', 'password': '123456'})
        assert_is_not_none(user)
        compare(c.read(user.id), user)
        compare(user.name, 'Anybody')

        c.delete(user.id)
        assert_is_none(c.read(user.id))
