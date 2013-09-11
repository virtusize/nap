# -*- coding: utf-8 -*-

from nap.authorization import Actions, Guard, Identity, Role, Permission, subject_alias, true_condition
from nap.model import Model
from tests.helpers import *


class Store(Model):
    pass


class AnyIdentity():
    pass


def test_subject_alias():
    assert_equal(subject_alias(Store), 'store')
    assert_equal(subject_alias(Store()), 'store')
    assert_equal(subject_alias('user'), 'user')


def test_actions():
    class SomeActions(Actions):
        this = 'this'
        that = 'that'
        both = Actions.alias(this, that)

    assert_equal(SomeActions.this, 'this')
    assert_equal(SomeActions.that, 'that')
    compare(SomeActions.both, ['this', 'that'])


def test_idendity():
    role = Role()
    role.grant('read', Store)

    i = Identity([role])

    assert_equal(len(i.roles), 1)
    compare(i.roles[0], role)

    role = Role()
    role.grant('write', Store)
    i.roles.append(role)

    assert_equal(len(i.roles), 2)
    compare(i.roles[1], role)


def test_basic_permission():
    read_store_permission = Permission('read', Store, true_condition)
    assert_true(read_store_permission.granted_on(Store(), AnyIdentity()))


def test_basic_role():
    role = Role()
    role.grant('read', Store)

    assert_equal(len(role.permissions), 1)


def test_multiple_actions_role():
    role = Role()
    role.grant(['read', 'write'], Store)

    assert_equal(len(role.permissions), 2)


def test_role_inheritance():
    role = Role()
    role.grant(['read', 'write'], Store)

    another_role = Role(inherit=[role])
    another_role.grant(['update', 'delete', 'query'], Store)

    assert_equal(len(role.permissions), 2)
    assert_equal(len(another_role.permissions), 5)


def test_permissions_without_conditions():
    guard = Guard()
    role = Role()
    role.grant('read', Store)
    identity = Identity([role])

    assert_true(guard.can(identity, 'read', Store))
    assert_true(guard.can(identity, 'read', Store()))

    assert_false(guard.cannot(identity, 'read', Store))
    assert_false(guard.cannot(identity, 'read', Store()))

def false_condition(subject, identity):
    return False


def is_the_same_condition(subject, identity):
    return subject.something == identity.something


def test_permissions_with_conditions():
    guard = Guard()
    role = Role()
    role.grant('read', Store)
    role.grant('write', Store, false_condition)
    identity = Identity([role])

    assert_true(guard.can(identity, 'read', Store))
    assert_false(guard.can(identity, 'write', Store))

    assert_false(guard.cannot(identity, 'read', Store))
    assert_true(guard.cannot(identity, 'write', Store))


def test_permissions_with_is_the_same_condition():
    guard = Guard()
    role = Role()
    role.grant('check_for_something', Store, is_the_same_condition)
    identity = Identity([role])
    identity.something = 'check'

    store = Store()
    store.something = 'check' 
    assert_true(guard.can(identity, 'check_for_something', store))
    store.something = 2
    assert_false(guard.can(identity, 'check_for_somethingone', store))
    store.something = True
    assert_false(guard.can(identity, 'check_for_somethingone', store))


def test_guard_with_multiple_roles():
    guard = Guard()

    role = Role()
    role.grant('read', Store)
    role.grant('write', Store)

    role2 = Role()
    role2.grant('delete', 'product')

    identity = Identity([role, role2])

    assert_true(guard.can(identity, 'read', Store))
    assert_false(guard.can(identity, 'read', 'anything'))
    assert_false(guard.can(identity, 'write', 'something'))
    assert_true(guard.can(identity, 'write', Store))
    assert_false(guard.can(identity, 'delete', Store))
    assert_true(guard.can(identity, 'delete', 'product'))
    assert_false(guard.can(identity, 'write', 'product'))


def test_predicate():
    guard = Guard()
    store = Store(owner_id=1)

    role = Role()
    role.grant('delete', Store, condition=lambda store, identity: identity.id == store.owner_id)

    valid_identity = Identity([role])
    valid_identity.id = 1

    invalid_identity = Identity([role])
    invalid_identity.id = 2

    assert_true(guard.can(valid_identity, 'delete', store))
    assert_false(guard.can(invalid_identity, 'delete', store))


def test_them_all():
    class SomeActions(Actions):
        read = 'read'
        write = 'write'
        manage = Actions.alias(read, write)

    class Roles(object):
        anonymous = Role()
        anonymous.grant(SomeActions.read, Store)

        owner = Role(inherit=[anonymous])
        owner.grant(SomeActions.manage, Store, is_the_same_condition)

    class SomethingIdentity(Identity):
        def __init__(self, roles, something):
            super(SomethingIdentity, self).__init__(roles)
            self.something = something

    guard = Guard()
    store = Store(something='check')

    identity = SomethingIdentity([Roles.anonymous], 'does not matter')
    assert_true(guard.can(identity, SomeActions.read, store))
    assert_false(guard.can(identity, SomeActions.write, store))

    identity = SomethingIdentity([Roles.owner], 'does matter')
    assert_true(guard.can(identity, SomeActions.read, store))
    assert_false(guard.can(identity, SomeActions.write, store))

    identity = SomethingIdentity([Roles.owner], 'check')
    assert_true(guard.can(identity, SomeActions.read, store))
    assert_true(guard.can(identity, SomeActions.write, store))
