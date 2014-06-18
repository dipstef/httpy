#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

settings = dict()

# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Topic :: Internet',
    'Topic :: Utilities',
]

settings.update(
    name='httpy',
    version='0.1',
    description='Http client with header parsing, connection checking and extended error reporting',
    long_description=open('README.rst').read(),
    author='Stefano Dipierro',
    license='Apache 2.0',
    url='https://github.com/dipstef/httpy',
    classifiers=CLASSIFIERS,
    keywords='http client exceptions exception error handling retry retrying headers content connection socket',
    packages=['httpy', 'httpy.connection', 'httpy.http', 'httpy.http.headers', 'httpy.requests'],
    test_suite='tests',
    requires=['unicoder', 'urlo']
)

setup(**settings)