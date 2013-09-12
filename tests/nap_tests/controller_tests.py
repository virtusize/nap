# -*- coding: utf-8 -*-
from nap.exceptions import UnsupportedMethodException, ModelNotFoundException, UnauthorizedException
from nap.controller import BaseController, ModelController
from nap.model import Model, Storage
from nap.authorization import Guard, Identity, Role

from tests.helpers import *


class SomeModel(Model):
    pass


class SomeModels(Storage):
    one = SomeModel(id=1, name='one')
    two = SomeModel(id=2, name='two')


class SomeModelController(ModelController):
    model = SomeModel
    model_storage = SomeModels


class SomeModelGuardController(ModelController):
    model = SomeModel
    model_storage = SomeModels
    guard = Guard()


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


def test_model_controller_index_with_context_kwarg():
    assert_equal(len(SomeModelController().index(context={})), 2)
    compare(SomeModelController().index(context={}), [SomeModels.one, SomeModels.two])


def test_model_controller_index_with_context_arg():
    assert_equal(len(SomeModelController().index({})), 2)
    compare(SomeModelController().index({}), [SomeModels.one, SomeModels.two])


def test_model_controller_read():
    compare(SomeModelController().read(SomeModels.one.id), SomeModels.one)


def test_model_controller_read_with_context_kwarg():
    compare(SomeModelController().read(SomeModels.one.id, context={}), SomeModels.one)


def test_model_controller_read_with_context_arg():
    compare(SomeModelController().read(SomeModels.one.id, {}), SomeModels.one)


@raises(ModelNotFoundException)
def test_model_controller_read_not_found():
    SomeModelController().read(3)


def test_model_guard_controller_read():
    role = Role()
    role.grant('read', SomeModel)
    identity = Identity([role])
    context = {'identity': identity}

    compare(SomeModelGuardController().read(SomeModels.one.id, context), SomeModels.one)


@raises(UnauthorizedException)
def test_model_guard_controller_read_unauthorized():
    role = Role()
    role.grant('something_else', SomeModel)
    identity = Identity([role])
    context = {'identity': identity}

    SomeModelGuardController().read(SomeModels.one.id, context)


def test_model_guard_controller_index():
    role = Role()
    role.grant('index', list)
    identity = Identity([role])
    context = {'identity': identity}

    assert_equal(len(SomeModelGuardController().index(context)), 2)
    assert_equal(len(SomeModelGuardController().index(context=context)), 2)


@raises(UnauthorizedException)
def test_model_guard_controller_read_unauthorized():
    role = Role()
    role.grant('something_else', SomeModel)
    identity = Identity([role])
    context = {'identity': identity}

    SomeModelGuardController().index(context)
