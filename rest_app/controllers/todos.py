# -*- coding: utf-8 -*-

from rest_app import app
from flask.ext.restful import Api, Resource

api = Api(app)

todos = [
    {'id': 1, 'title': 'Get shit done …'},
    {'id': 2, 'title': 'Get more shit done …'},
    {'id': 3, 'title': 'Get even more shit done …'}
]


class Todo(Resource):
    def get(self, todo_id):
        for todo in todos:
            if todo['id'] == int(todo_id):
                return todo
        return None


class TodoList(Resource):
    def get(self):
        return todos

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<string:todo_id>')
