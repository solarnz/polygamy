#!/usr/bin/env python

from setuptools import setup

setup(
    name='gmrh',
    version='0.1-dev',
    packages=['gmrh'],
    entry_points={
        'console_scripts': [
            'gmrh = gmrh:main'
        ]
    },

    author='Christopher Trotman',
    author_email='chris+gmrh@trotman.io'
)
