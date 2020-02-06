#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import setup, find_packages

import itertools as it

# the basic needed requirements for a package
base_requirements = []

# extras requirements list

# SNIPPET: example extra requirement
# example_extra_requirements = ['requests']
# extras = [example_extra_requirements,]

# Add your extra requirements lists here:
extras = [
]

# combination of all the extras requirements
_all_requirements = [[base_requirements]] + extras
all_requirements = it.chain.from_iterable(_all_requirements)

setup(
    name='{{ cookiecutter.project_name }}',
    version='{{ cookiecutter.initial_version }}',
    author="{{ cookiecutter.owner_name }}",
    author_email="{{ cookiecutter.owner_email }}",
    description="{{ cookiecutter.project_description }}",
    #long_description=open('README.org').read(),
    license="{{ cookiecutter.license }}",
    url="{{ cookiecutter.url }}",
    classifiers=[
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3'
    ],
    # building/dev
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'tox'],

    # package
    packages=find_packages(where='src'),

    package_dir={'' : 'src'},

    # if this is true then the package_data won't be included in the
    # dist. Use MANIFEST.in for this
    include_package_data=True,

    # pymodules is for single file standalone modules not part of the
    # package
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],

    entry_points={
        'console_scripts' : [
            '{{ cookiecutter.project_slug }}={{ cookiecutter.project_slug }}.cli:cli',
        ]
    },

    install_requires=base_requirements,

    # SNIPPET: example of using extra requirements
    # extras_require={
    #     'extras' : example_extra_requirements
    #     'all' : all_requirements,
    # }

    # include your extra requirement sets here
    extras_require={
        'all' : all_requirements,
    }
)
