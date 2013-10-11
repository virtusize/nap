# -*- coding: utf-8 -*-
from nap.exceptions import ModelNotFoundException, ModelInvalidException, UnauthorizedException
from nap.authorization import Guard, Role, ControllerActions, Identity
from nap.util import Context
from sa_nap.controller import SAModelController
from tests.fixtures import Users, User, Stores, Store, Products, Product, fixture_loader, ProductTypes
from tests.helpers import *


class UserController(SAModelController):
    model = User
    session_factory = db_session


class StoreController(SAModelController):
    model = Store
    session_factory = db_session


class ProductController(SAModelController):
    model = Product
    session_factory = db_session
    guard = Guard()


def test_controller():
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        c = UserController()

        user = c.read(1)
        assert_is_not_none(user)

        email = 'somebody@example.com'
        c.update(user.id, {'email': email})

        user = c.read(1)
        compare(user.email, email)

        user = c.create({'name': u'Anybody', 'email': 'anybody@example.com', 'password': '123456'})
        assert_is_not_none(user)
        compare(c.read(user.id), user)
        compare(user.name, 'Anybody')


@raises(ModelNotFoundException)
def test_controller_delete():
    with db(), fixtures(Users, fixture_loader=fixture_loader):
        c = UserController()

        c.delete(Users.john.id)
        c.read(Users.john.id)


@raises(ModelInvalidException)
def test_unique_validator_by_db_insert_same_commit():
    with db():
        c = UserController()
        c.create({'name': u'Joe', 'email': 'valid@example.com', 'password': '123456'})
        c.create({'name': u'Other Joe', 'email': 'valid@example.com', 'password': '123456'})


@raises(UnauthorizedException)
def test_unauthorized_index_permission():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        c = ProductController()
        c.index()


@raises(UnauthorizedException)
def test_unauthorized_read_permission():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        c = ProductController()
        c.read(1)


@raises(UnauthorizedException)
def test_unauthorized_update_permission():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        c = ProductController()
        c.update(1, {'name': u'Blue Shirt', 'product_type_id': ProductTypes.shirt.id})


@raises(UnauthorizedException)
def test_unauthorized_create_permission():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        c = ProductController()
        c.create({'name': u'Red Pants', 'product_type_id': ProductTypes.pants.id, 'store_id': Stores.virtusize.id})


@raises(UnauthorizedException)
def test_unauthorized_delete_permission():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        c = ProductController()
        c.delete(1)


def test_index_permission():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        ctx = Context()
        role = Role()
        role.grant(ControllerActions.index, Product)
        ctx.identity = Identity([role])
        c = ProductController()
        c.index(ctx)


def test_read_permission():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        ctx = Context()
        role = Role()
        role.grant(ControllerActions.read, Product)
        ctx.identity = Identity([role])
        c = ProductController()
        c.read(1, ctx)


def test_update_permission():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        ctx = Context()
        role = Role()
        role.grant(ControllerActions.update, Product)
        ctx.identity = Identity([role])
        c = ProductController()
        c.update(1, {'name': u'Blue Shirt', 'product_type_id': ProductTypes.shirt.id}, ctx)


def test_create_permission():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        ctx = Context()
        role = Role()
        role.grant(ControllerActions.create, Product)
        ctx.identity = Identity([role])
        c = ProductController()
        c.create({'name': u'Red Pants', 'product_type_id': ProductTypes.pants.id, 'store_id': Stores.virtusize.id}, ctx)


def test_delete_permission():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        ctx = Context()
        role = Role()
        role.grant(ControllerActions.delete, Product)
        ctx.identity = Identity([role])
        c = ProductController()
        c.delete(1, ctx)


def test_empty_list_index_permission():
    with db(), fixtures(Products, fixture_loader=fixture_loader):
        ctx = Context()
        role = Role()
        role.grant(ControllerActions.index, Product)
        role.grant(ControllerActions.delete, Product)
        ctx.identity = Identity([role])
        c = ProductController()
        c.delete(1, ctx)

        compare(c.index(ctx), [])
