# -*- coding: utf-8 -*-


def subject_alias(subject):
    if isinstance(subject, basestring):
        return subject
    elif isinstance(subject, type):
        return subject.__name__.lower()
    else:
        return type(subject).__name__.lower()


class Guard:
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


class Identity:

    def __init__(self, roles):
        self.roles = roles


class Role:
    def __init__(self, *args, **kwargs):
        self.permissions = []

    def grant(self, *args, **kwargs):
        self.permissions.append(Permission(*args, **kwargs))


def true_condition(self, *args, **kwargs):
    return True


class Permission:

    def __init__(self, action, subject, condition=true_condition):
        self.action = action
        self.subject = subject_alias(subject)
        self.condition = condition

    @property
    def key(self):
        return (self.action, self.subject)

    def granted_on(self, subject, identity):
        return self.condition(subject, identity)
