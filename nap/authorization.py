# -*- coding: utf-8 -*-
"""
Hannes,

I think we need an Action class, partly to allow to use non string "actions"
an partly because we need support for "umbrella" actions such as "manage"
"moderate" etc...

But we also want to bea able to just use strings to identify actions and
to allow future users of API to define custom actions.

So I am thinking:

class CRUDActions(ActionsContainer):

    read = Action()
    create = Action()
    update = Action()
    delete = Action()

class ExtendedCRUDActions(CRUDActions):

    manage = Action()
    manage.include(CRUDActions.read, CRUDActions.write, ...)

    ##Need to test if this kind of inheritance works.

class Roles(object):

    guest = Role()
    guest.grant('read', Store)
    guest.grant(CRUDActions.write, 'store')

    admin = Role()
    admin.inherit(guest)
    admin.grant('manage', 'store')


Then the Guard needs to be initialized with all the roles, and actions.

like this:

guard = Guard(ExtendedCRUDActions, Roles)

or even better:

MyAppGuard(Guard):
    actions = ExtendedCRUDActions
    roles = Roles

class MyAPI(Api):
    guard = MyAppGuard

## Not sure about where to put the guard, maybe on API or controller?!
## Prolly better on controller, even if it is repetitive.

"""

from inflection import underscore


def subject_alias(subject):
    if isinstance(subject, basestring):
        return underscore(subject)
    elif isinstance(subject, type):
        return underscore(subject.__name__)
    else:
        return underscore(type(subject).__name__)


class Guard(object):
    """
    Identity is the base class for users, roles, services, etc.
    Identity provides a set of permissions.
    """

    def can(self, identity, action, subject):
        subject_name = subject_alias(subject)
        key_set = set([(action, subject_name), (action, 'all'), ('manage', subject_name), ('manage', 'all')])

        for role in identity.roles:
            for permission in role.permissions:
                if permission.key in key_set and permission.granted_on(subject, identity):
                    return True

        return False


class Identity(object):

    def __init__(self, roles):
        self.roles = roles


class Role(object):
    def __init__(self, *args, **kwargs):
        self.permissions = []

    def grant(self, *args, **kwargs):
        self.permissions.append(Permission(*args, **kwargs))
        return self


def true_condition(self, *args, **kwargs):
    return True


class Permission(object):

    def __init__(self, action, subject, condition=true_condition):
        self.action = action
        self.subject = subject_alias(subject)
        self.condition = condition

    @property
    def key(self):
        return (self.action, self.subject)

    def granted_on(self, subject, identity):
        return self.condition(subject, identity)
