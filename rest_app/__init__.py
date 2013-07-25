# -*- coding: utf-8 -*-

from flask import Flask
app = Flask(__name__)

import rest_app.controllers
import rest_app.python_client
