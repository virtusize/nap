# -*- coding: utf-8 -*-

from flask import Flask, g, request
from flask_nap.api import Api, Debug, JsonRequestParser, ApiMixin
from flask_nap.view import ModelView, route
from flask_nap.view_filters import CamelizeFilter, ExcludeFilter
from flask_nap.exception_handlers import UnsupportedMethodExceptionHandler, ModelNotFoundExceptionHandler, ModelInvalidExceptionHandler, UnauthorizedExceptionHandler, UnauthenticatedExceptionHandler, HTTPExceptionHandler, InvalidJSONExceptionHandler, InvalidMimetypeExceptionHandler
from sa_nap.controller import SAModelController
from sa_nap.model import SAModelSerializer
from tests.fixtures import ProductType, ProductTypes, Store, User, Product
from tests.helpers import db_session
from nap.model import ModelSerializer
from nap.controller import ModelController
from nap.authorization import Guard, ControllerActions, Role, Identity


class ProductTypeController(ModelController):
    model = ProductType
    model_storage = ProductTypes


class ProductTypeView(ModelView):
    controller = ProductTypeController
    filter_chain = [CamelizeFilter]
    serializer = ModelSerializer


class StoreController(SAModelController):
    model = Store
    session_factory = db_session

    def query_by_owner(self, owner_id):
        return self.db_session.query(self.model).filter(Store.owner_id==owner_id).all()


class UserController(SAModelController):
    model = User
    session_factory = db_session
    guard = Guard()


class UserView(ModelView):
    controller = UserController
    filter_chain = [ExcludeFilter(['password']), CamelizeFilter]
    serializer = SAModelSerializer


class StoreView(ModelView):
    controller = StoreController
    filter_chain = [CamelizeFilter]
    serializer = SAModelSerializer

    @route(rule='/users/<int:owner_id>/stores/', methods=['GET'])
    def index_by_owner(self, owner_id):
        return self.controller.query_by_owner(owner_id), 200


class ProductController(SAModelController):
    model = Product
    session_factory = db_session


class ProductView(ModelView):
    controller = ProductController
    filter_chain = [CamelizeFilter]
    serializer = SAModelSerializer


class Roles(object):
    guest = Role()
    guest.grant(ControllerActions.index, User)
    guest.grant(ControllerActions.read, User)


class GuestIdentity(Identity):
    def __init__(self):
        super(GuestIdentity, self).__init__([Roles.guest])


class Authentication(ApiMixin):
    def before(self):
        if request.headers.has_key('Authorization') and request.headers.get('Authorization', None) == '123xyz':
            g.ctx.identity = GuestIdentity()


class AnApi(Api):
    name = 'api'
    prefix = '/api'
    version = 1
    mixins = [
        Authentication,
        Debug(print_request=False, print_response=False),
        JsonRequestParser
    ]
    views = [
        ProductTypeView,
        ProductView,
        StoreView,
        UserView
    ]
    exception_handlers = [
        UnsupportedMethodExceptionHandler,
        InvalidJSONExceptionHandler,
        InvalidMimetypeExceptionHandler,
        ModelNotFoundExceptionHandler,
        ModelInvalidExceptionHandler,
        UnauthorizedExceptionHandler,
        UnauthenticatedExceptionHandler
    ]


an_api = AnApi()
app = Flask(__name__)
app.register_blueprint(an_api)

HTTPExceptionHandler.register_on(app, an_api)
