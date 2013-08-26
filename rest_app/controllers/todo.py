# -*- coding: utf-8 -*-

from flask.views import MethodView


class ToDoView(MethodView):

    def get(self):
        return session.get('counter', 0)

    def post(self):
        session['counter'] = session.get('counter', 0) + 1
        return 'OK'
