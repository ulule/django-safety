# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, find_packages

version = __import__('safety').__version__

root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(root, 'README.rst')) as f:
    README = f.read()

setup(
    name='django-safety',
    version=version,
    description='Django application to control user sessions',
    long_description=README,
    author='Gilles Fabio',
    author_email='gilles.fabio@gmail.com',
    url='http://github.com/ulule/django-safety',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'six',
        'ua-parser',
        'GeoIP',
        'geoip2',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ]
)
