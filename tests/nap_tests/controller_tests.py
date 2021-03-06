# -*- coding: utf-8 -*-
from nap.exceptions import UnsupportedMethodException, ModelNotFoundException, UnauthorizedException
from nap.controller import BaseController, ModelController
from nap.model import Model, Storage
from nap.authorization import Guard, Identity, Role
from nap.util import Context

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


def test_base_controller_model_name():
    bc = BaseController()
    assert_equal(bc.model_name, 'BaseController')

    bc.model = SomeModel
    assert_equal(bc.model_name, 'SomeModel')


def test_base_controller_authorize():
    bc = BaseController()
    model = 'something'
    ctx = Context()
    assert_equal(bc.authorize(ctx, 'read', model), model)


@raises(UnauthorizedException)
def test_base_controller_authorize_no_ctx():
    bc = BaseController()
    model = 'something'
    bc.guard = Guard()
    ctx = None
    bc.authorize(ctx, 'read', model)


@raises(UnauthorizedException)
def test_base_controller_authorize_no_identity():
    bc = BaseController()
    model = 'something'
    bc.guard = Guard()
    ctx = Context()
    bc.authorize(ctx, 'read', model)


@raises(UnauthorizedException)
def test_base_controller_authorize_no_role():
    bc = BaseController()
    model = 'something'
    bc.guard = Guard()
    ctx = Context()
    ctx.identity = Identity([])
    bc.authorize(ctx, 'read', model)


def test_base_controller_authorize_successful():
    bc = BaseController()
    model = SomeModel()
    bc.guard = Guard()
    bc.model = SomeModel
    ctx = Context()
    role = Role()
    role.grant('read', SomeModel)
    ctx.identity = Identity([role])
    bc.authorize(ctx, 'read', model)


def test_model_controller_index():
    assert_equal(len(SomeModelController().index()), 2)
    compare(SomeModelController().index(), [SomeModels.one, SomeModels.two])


def test_model_controller_fetch_all():
    assert_equal(len(SomeModelController().fetch_all()), 2)
    compare(SomeModelController().fetch_all(), [SomeModels.one, SomeModels.two])


def test_model_controller_index_with_ctx_kwarg():
    assert_equal(len(SomeModelController().index(ctx={})), 2)
    compare(SomeModelController().index(ctx={}), [SomeModels.one, SomeModels.two])


def test_model_controller_index_with_ctx_arg():
    assert_equal(len(SomeModelController().index({})), 2)
    compare(SomeModelController().index({}), [SomeModels.one, SomeModels.two])


def test_model_controller_read():
    compare(SomeModelController().read(SomeModels.one.id), SomeModels.one)


def test_model_controller_fetch_model():
    compare(SomeModelController().fetch_model(SomeModels.one.id), SomeModels.one)


def test_model_controller_read_with_ctx_kwarg():
    compare(SomeModelController().read(SomeModels.one.id, ctx={}), SomeModels.one)


def test_model_controller_read_with_ctx_arg():
    compare(SomeModelController().read(SomeModels.one.id, {}), SomeModels.one)


@raises(ModelNotFoundException)
def test_model_controller_read_not_found():
    SomeModelController().read(3)


@raises(ModelNotFoundException)
def test_model_controller_fetch_model_not_found():
    SomeModelController().fetch_model(3)


def test_model_guard_controller_read():
    role = Role()
    role.grant('read', SomeModel)
    identity = Identity([role])
    ctx = Context()
    ctx.identity = identity

    compare(SomeModelGuardController().read(SomeModels.one.id, ctx), SomeModels.one)


@raises(UnauthorizedException)
def test_model_guard_controller_read_unauthorized():
    role = Role()
    role.grant('something_else', SomeModel)
    identity = Identity([role])
    ctx = Context()
    ctx.identity = identity

    SomeModelGuardController().read(SomeModels.one.id, ctx)


@raises(UnauthorizedException)
def test_model_guard_controller_read_missing_identity():
    SomeModelGuardController().read(SomeModels.one.id, Context())


def test_model_guard_controller_index():
    role = Role()
    role.grant('index', SomeModel)
    identity = Identity([role])
    ctx = Context()
    ctx.identity = identity

    assert_equal(len(SomeModelGuardController().index(ctx)), 2)
    assert_equal(len(SomeModelGuardController().index(ctx=ctx)), 2)


@raises(UnauthorizedException)
def test_model_guard_controller_index_unauthorized():
    role = Role()
    role.grant('something_else', SomeModel)
    identity = Identity([role])
    ctx = Context()
    ctx.identity = identity

    SomeModelGuardController().index(ctx)


@raises(UnauthorizedException)
def test_model_guard_controller_index_wrong_model():
    class OtherModel(Model):
        pass

    role = Role()
    role.grant('read', OtherModel)
    identity = Identity([role])
    ctx = Context()
    ctx.identity = identity

    SomeModelGuardController().index(ctx)
