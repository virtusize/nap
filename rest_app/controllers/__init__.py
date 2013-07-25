# -*- coding: utf-8 -*-

from flask import jsonify, json
from rest_app import app
from rest_app.python_client import Client


@app.route('/')
def index():
    return "Hello world!"


@app.route('/todos-test')
def todos_test():
    c = Client()
    return jsonify(todos=c.todos.all())


@app.route('/todo-test')
def todo_test():
    c = Client()
    return jsonify(c.todos.get(1))

import todos
