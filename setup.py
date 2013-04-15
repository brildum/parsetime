#!/usr/bin/env python

import setuptools

setuptools.setup(
    name='parsetime',
    description='Parse timestamps from strings',
    version='0.1',
    install_requires=[
        'python-dateutil==2.1',
    ],
    py_modules=[
        'parsetime',
    ],
    test_suite='tests.suite',
    author='Chris Carroll',
    author_email='brildum@gmail.com',
    url='http://github.com/brildum/parsetime',
)
