# -*- coding: utf-8 -*-

from flask import Flask
from flask_rest_api import Api, Debug, JsonEncoder, ModelView
from core.model import Model, Storage
from tests.core_tests.database_fixtures import ProductType, ProductTypes
from core.model.controller import ModelController
from core.validation.validators import *

app = Flask(__name__)


api = Api('api', '/api', 1)

Debug(api, print_request=False, print_response=False)

JsonEncoder(api)
#JsonDecoder(api)
#MethodOverride(api)
#Authentication(api)

product_type_controller = ModelController(ProductType, ProductTypes)
product_type_view = ModelView(product_type_controller)

product_type_view.register_on(api)

app.register_blueprint(api)
