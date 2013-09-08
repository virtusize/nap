# -*- coding: utf-8 -*-

from flask import Flask
from flask_nap.api import Api, Debug, JsonEncoder, JsonDecoder
from flask_nap.view import ModelView, CamelizeFilter, ExcludeFilter
from sa_nap.controller import SAModelController
from sa_nap.model import SAModelSerializer
from tests.fixtures import ProductType, ProductTypes, Store, User
from tests.helpers import db_session
from nap.model import ModelSerializer
from nap.controller import ModelController


app = Flask(__name__)


api = Api('api', '/api', 1)

Debug(api, print_request=False, print_response=False)

JsonEncoder(api)
JsonDecoder(api)
#MethodOverride(api)
#Authentication(api)


class ProductTypeController(ModelController):
    model = ProductType
    model_storage = ProductTypes

#
# class ProductTypeView(ModelView):
#     controller = ProductTypeController
#     filter_chain = [CamelizeFilter()]
#     serializer = ModelSerializer()


product_type_view = ModelView(ProductTypeController(), filter_chain=[CamelizeFilter()], serializer=ModelSerializer())
product_type_view.register_on(api)


class StoreController(SAModelController):
    model = Store
    session_factory = db_session

store_view = ModelView(StoreController(), filter_chain=[CamelizeFilter()], serializer=SAModelSerializer())
store_view.register_on(api)


class UserController(SAModelController):
    model = User
    session_factory = db_session

user_view = ModelView(UserController(), filter_chain=[ExcludeFilter(['password']), CamelizeFilter()], serializer=SAModelSerializer())
user_view.register_on(api)

app.register_blueprint(api)


