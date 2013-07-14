#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='gmrh',
    version='0.1-dev',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'gmrh = gmrh:start_func'
        ]
    },

    author='Christopher Trotman',
    author_email='chris+gmrh@trotman.io'
)
