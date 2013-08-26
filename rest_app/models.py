#!/usr/bin/python
# -*- coding: utf-8 -*-


from sqlalchemy import Column, Integer, String
from core.database import DbModel
from core.validation import PresenceValidator


class Store(DbModel):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    short_name = Column(String)


class User(DbModel):

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    _validate_with = [PresenceValidator('name'), PresenceValidator('email')]


u = User(email='asdasd')
result = u.validate()
print result.errors
assert result.valid
