#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(

    name='nap',
    version='0.2.0',
    description='Nap. A Python API framework with support for Flask and SQLAlchemy.',
    author='Virtusize AB',
    author_email='contact@virtusize.com',
    url='http://www.virtusize.com/',

    packages=find_packages(),

    install_requires=[
        'blinker',
        'coverage',
        'dogpile.cache==0.5.0',
        'flask==0.10.1',
        'fixture',
        'inflection',
        'nose',
        'requests',
        'sqlalchemy==0.8.2',
        'testfixtures'
    ]
)
