# -*- coding: utf-8 -*-

from rest_app import app

@app.route('/')
def index():
    return "Hello world!"
