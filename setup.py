#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
setup(

    name='rest-poc',
    version='0.0.1',
    packages=find_packages(),

    install_requires=[
        'flask',
        'fixture',
        'inflection',
        'nose',
        'sqlalchemy'
    ]
)
