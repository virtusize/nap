# -*- coding: utf-8 -*-

from flask import Flask
from flask_nap.api import Api, Debug, JsonDecoder
from flask_nap.view import ModelView
from flask_nap.view_filters import CamelizeFilter, ExcludeFilter
from flask_nap.exception_handlers import UnsupportedMethodExceptionHandler, ModelNotFoundExceptionHandler, ModelInvalidExceptionHandler
from sa_nap.controller import SAModelController
from sa_nap.model import SAModelSerializer
from tests.fixtures import ProductType, ProductTypes, Store, User, Product
from tests.helpers import db_session
from nap.model import ModelSerializer
from nap.controller import ModelController


class ProductTypeController(ModelController):
    model = ProductType
    model_storage = ProductTypes
    #guard = Guard


class ProductTypeView(ModelView):
    controller = ProductTypeController
    filter_chain = [CamelizeFilter]
    serializer = ModelSerializer


class StoreController(SAModelController):
    model = Store
    session_factory = db_session
    #guard = Guard


class StoreView(ModelView):
    controller = StoreController
    filter_chain = [CamelizeFilter]
    serializer = SAModelSerializer


class UserController(SAModelController):
    model = User
    session_factory = db_session
    #guard = Guard


class UserView(ModelView):
    controller = UserController
    filter_chain = [ExcludeFilter(['password']), CamelizeFilter]
    serializer = SAModelSerializer


class ProductController(SAModelController):
    model = Product
    session_factory = db_session
    #guard = Guard


class ProductView(ModelView):
    controller = ProductController
    filter_chain = [CamelizeFilter]
    serializer = SAModelSerializer


class AnApi(Api):
    name = 'api'
    prefix = '/api'
    version = 1
    mixins = [
        Debug(print_request=False, print_response=False),
        JsonDecoder,
        #MethodOverride
        #Authentication
    ]
    views = [
        ProductTypeView,
        StoreView,
        UserView
    ]
    exception_handlers = [
        UnsupportedMethodExceptionHandler,
        ModelNotFoundExceptionHandler,
        ModelInvalidExceptionHandler
    ]

an_api = AnApi()
app = Flask(__name__)
app.register_blueprint(an_api)
