# -*- coding: utf-8 -*-

from flask import Flask
from flask_rest_api import Api, Debug, JsonEncoder, JsonDecoder, ModelView, SAModelFilter
from core.database import SAModelController
from tests.core_tests.database_fixtures import ProductType, ProductTypes, Store
from tests.helpers import db_session
from core.model.controller import ModelController
from core.validation.validators import *

app = Flask(__name__)


api = Api('api', '/api', 1)

Debug(api, print_request=True, print_response=False)

JsonEncoder(api)
JsonDecoder(api)
#MethodOverride(api)
#Authentication(api)

product_type_controller = ModelController(ProductType, ProductTypes)
product_type_view = ModelView(product_type_controller)
product_type_view.register_on(api)

store_controller = SAModelController(Store, db_session)
store_view = ModelView(store_controller, filter_chain=[SAModelFilter()])
store_view.register_on(api)

app.register_blueprint(api)
