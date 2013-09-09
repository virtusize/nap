# -*- coding: utf-8 -*-
from nap.exceptions import UnsupportedMethodException, ModelNotFoundException
from nap.controller import BaseController, ModelController
from nap.model import Model, Storage

from tests.helpers import *


class SomeModel(Model):
    pass


class SomeModels(Storage):
    one = SomeModel(id=1, name='one')
    two = SomeModel(id=2, name='two')


class SomeModelController(ModelController):
    model = SomeModel
    model_storage = SomeModels


@raises(UnsupportedMethodException)
def test_base_controller_index():
    BaseController().index()


@raises(UnsupportedMethodException)
def test_base_controller_read():
    BaseController().read(1)


@raises(UnsupportedMethodException)
def test_base_controller_create():
    BaseController().create({})


@raises(UnsupportedMethodException)
def test_base_controller_update():
    BaseController().update(1, {})


@raises(UnsupportedMethodException)
def test_base_controller_delete():
    BaseController().delete(1)


@raises(UnsupportedMethodException)
def test_base_controller_query():
    BaseController().query({})


def test_model_controller_index():
    assert_equal(len(SomeModelController().index()), 2)
    compare(SomeModelController().index(), [SomeModels.one, SomeModels.two])


def test_model_controller_read():
    compare(SomeModelController().read(SomeModels.one.id), SomeModels.one)


@raises(ModelNotFoundException)
def test_model_controller_read_not_found():
    SomeModelController().read(3)
