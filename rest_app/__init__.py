# -*- coding: utf-8 -*-

import rest_app.models
from flask import Flask
from core.database import DbModel, engine
from fixtures import Stores, Users

app = Flask(__name__)


DbModel.metadata.create_all(engine)

from fixture import SQLAlchemyFixture, TrimmedNameStyle
db_fixture = SQLAlchemyFixture(env=models, style=TrimmedNameStyle(suffix='s'), engine=engine)
db_fixture.data(Stores, Users).setup()

import rest_app.controllers