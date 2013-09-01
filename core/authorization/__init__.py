#!/usr/bin/python
# -*- coding: utf-8 -*-


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