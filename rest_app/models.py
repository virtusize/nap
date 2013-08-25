#!/usr/bin/python
# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String
from core.database import DbModel


class Store(DbModel):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    short_name = Column(String)


class User(DbModel):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
