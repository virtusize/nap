# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

from sqlalchemy import create_engine

import core
from core import DbModel

engine = create_engine('sqlite:///:memory:', echo=True)
DbModel.metadata.create_all(engine)

#from fixture import SQLAlchemyFixture, TrimmedNameStyle
#from fixtures import Stores, Users
#db_fixture = SQLAlchemyFixture(env=core, style=TrimmedNameStyle(suffix='s'), engine=engine)
#db_fixture.data(Stores, Users).setup()

import rest_app.controllers
import core
import models
#import fixtures
