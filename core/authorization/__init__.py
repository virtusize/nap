#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Taking inspiration from rails and other frameworks:


I would like to have something like this in the business layer:

ModelGuard():

    guest = Role()
    guast.can(Action.read, AnyModel)

    admin = Role()
    admin.can(Actions.manage, Store)

    store_owner = Role()
    store_owner.can(Actions.manage, Store, if=is_store_owner)


guard = ModelGuard()

guard.can(user, Actions.read, model) --> True/False

"""


class Identity:
    """
    Identity is the base class for users, roles, services, etc.
    Identity provides a set of permissions.
    """
    pass


class Guard:
    """
    Default guard, subclass this to implement
    resource specific guards.
    """

    def can(self, *args, **kwargs):
        raise NotImplementedError