# -*- coding: utf-8 -*-

from rest_app import app
from rest_app.models import Store, User


@app.route('/')
def index():
    user = User(name='Hannes')
    return "Hello " + user.name + "!"

