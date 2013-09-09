# -*- coding: utf-8 -*-

from flask import Flask
from flask_nap.api import Api, Debug, JsonEncoder, JsonDecoder
from flask_nap.view import ModelView
from flask_nap.view_filters import CamelizeFilter, ExcludeFilter
from sa_nap.controller import SAModelController
from sa_nap.model import SAModelSerializer
from tests.fixtures import ProductType, ProductTypes, Store, User
from tests.helpers import db_session
from nap.model import ModelSerializer
from nap.controller import ModelController


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


class StoreView(ModelView):
    controller = StoreController
    filter_chain = [CamelizeFilter]
    serializer = SAModelSerializer


class UserController(SAModelController):
    model = User
    session_factory = db_session


class UserView(ModelView):
    controller = UserController
    filter_chain = [ExcludeFilter(['password']), CamelizeFilter]
    serializer = SAModelSerializer


class AnApi(Api):
    name = 'api'
    prefix = '/api'
    version = 1
    mixins = [
        Debug(print_request=False, print_response=False),
        JsonEncoder,
        JsonDecoder,
        #MethodOverride(api)
        #Authentication(api)
    ]
    views = [
        ProductTypeView,
        StoreView,
        UserView
    ]

an_api = AnApi()
app = Flask(__name__)
app.register_blueprint(an_api)
