# -*- coding: utf-8 -*-


class Model(object):

    @classmethod
    def _create(cls, data, context):
        raise NotImplementedError()

    @classmethod
    def _read(cls, id, context):
        raise NotImplementedError()

    @classmethod
    def _update(cls, id, data, context):
        raise NotImplementedError()

    @classmethod
    def _delete(cls, id, context):
        raise NotImplementedError()


class TableLessModel(Model):
    pass
