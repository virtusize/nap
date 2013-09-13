#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(

    name='nap',
    version='0.1.0',
    description='Nap. A Python API framework with support for Flask and SQLAlchemy.',
    author='Virtusize AB',
    author_email='contact@virtusize.com',
    url='http://www.virtusize.com/',

    packages=find_packages(),

    install_requires=[
        'coverage',
        'flask',
        'fixture',
        'inflection',
        'nose',
        'sqlalchemy',
        'testfixtures',
    ]
)
