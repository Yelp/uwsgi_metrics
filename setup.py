#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

setup(
    name='uwsgi_metrics',
    version='0.2.0',
    description='Metrics for uWSGI services',
    author='John Billings',
    author_email='billings@yelp.com',
    url='https://gitweb.yelpcorp.com/?p=uwsgi_metrics.git',
    packages=find_packages(exclude=['tests']),
    setup_requires=['setuptools'],
    install_requires=[
        'treap',
    ],
    license='Copyright Yelp 2013, All Rights Reserved'
)
