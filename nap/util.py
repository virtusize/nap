#!/usr/bin/python
# -*- coding: utf-8 -*-
import types


def ensure_instance(cls_or_instance):
    """
    Makes sure that we always have an instance,
    if passed a class, assume it has a default constructor
    and instantiate it.
    """
    if isinstance(cls_or_instance, (type, types.ClassType)):
        return cls_or_instance()
    else:
        return cls_or_instance