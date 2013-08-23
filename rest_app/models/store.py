# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String

from core import DbModel


class Store(DbModel):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    short_name = Column(String)
