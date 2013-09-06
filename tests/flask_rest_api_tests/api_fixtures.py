# -*- coding: utf-8 -*-

from flask import Flask
from flask_nap import Api, Debug, JsonEncoder, JsonDecoder, ModelView
from sa_nap.controller import SAModelController
from sa_nap.model import SAModelSerializer
from tests.core_tests.database_fixtures import ProductType, ProductTypes, Store
from tests.helpers import db_session
from nap.model import ModelSerializer
from nap.controller import ModelController


app = Flask(__name__)


api = Api('api', '/api', 1)

Debug(api, print_request=True, print_response=False)

JsonEncoder(api)
JsonDecoder(api)
#MethodOverride(api)
#Authentication(api)

product_type_controller = ModelController(ProductType, ProductTypes)
product_type_view = ModelView(product_type_controller, serializer=ModelSerializer())
product_type_view.register_on(api)

store_controller = SAModelController(Store, db_session)
store_view = ModelView(store_controller, filter_chain=[], serializer=SAModelSerializer())
store_view.register_on(api)

app.register_blueprint(api)
