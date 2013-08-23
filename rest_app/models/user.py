# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String

from core import DbModel


class User(DbModel):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
