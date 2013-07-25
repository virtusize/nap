#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
setup(

    name='vs-rest-poc',
    version='0.0.1',
    packages=find_packages(),

    install_requires=[
        'flask==0.10.1'
    ]
)
