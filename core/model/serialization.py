#!/usr/bin/python
# -*- coding: utf-8 -*-


def dict_or_state(model_instance):
    if hasattr(model_instance, '__getstate__'):
        return model_instance.__getstate__()

    return model_instance.__dict__


def exclude(exclude_list):

    def strategy(model_instance):
        data = dict(dict_or_state(model_instance))
        for field in exclude_list:
            del data[field]
        return data

    return strategy