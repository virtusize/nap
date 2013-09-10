# -*- coding: utf-8 -*-

from nap.authorization import Guard, Identity, Role, Permission, subject_alias
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
    read_store_permission = Permission('read', Store)
    assert_true(read_store_permission.granted_on(Store(), AnyIdentity()))


def test_basic_role():
    role = Role()
    role.grant('read', Store)

    assert_equal(len(role.permissions), 1)

def test_permissions_without_conditions():
    guard = Guard()
    role = Role()
    role.grant('read', Store)
    identity = Identity([role])

    assert_true(guard.can(identity, 'read', Store))
    assert_true(guard.can(identity, 'read', Store()))

    role = Role()
    role.grant('manage', Store)
    identity = Identity([role])
    assert_true(guard.can(identity, 'read', Store))
    assert_true(guard.can(identity, 'write', Store))
    assert_true(guard.can(identity, 'other_stuff', Store))
    assert_false(guard.can(identity, 'read', 'user'))

    role = Role()
    role.grant('read', 'all')
    identity = Identity([role])
    assert_true(guard.can(identity, 'read', Store))
    assert_true(guard.can(identity, 'read', Store()))
    assert_false(guard.can(identity, 'write', Store))

    role = Role()
    role.grant('manage', 'all')
    identity = Identity([role])
    assert_true(guard.can(identity, 'read', Store))
    assert_true(guard.can(identity, 'write', Store()))
    assert_true(guard.can(identity, 'something', 'anything'))


def test_guard_with_multiple_roles():
    guard = Guard()

    role = Role()
    role.grant('read', 'all')
    role.grant('write', Store)

    role2 = Role()
    role2.grant('delete', 'product')

    identity = Identity([role, role2])

    assert_true(guard.can(identity, 'read', Store))
    assert_true(guard.can(identity, 'read', 'anything'))
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


