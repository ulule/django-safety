# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, find_packages

root = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(root, 'README.rst')) as f:
    readme = f.read()

version = __import__('safety').__version__

install_requires = [
    'six',
    'ua-parser',
    'geoip2'
]

setup(
    name='django-safety',
    version=version,
    description='Generic Django application for safer user accounts',
    long_description=readme,
    author='Gilles Fabio',
    author_email='gilles.fabio@gmail.com',
    url='http://github.com/ulule/django-safety',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
