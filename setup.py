#!/usr/bin/env python

from setuptools import setup

setup(
    name='gmrh',
    version='0.1.1-dev',
    packages=['gmrh'],
    entry_points={
        'console_scripts': [
            'gmrh = gmrh:main'
        ]
    },
    install_requires=[
        'blessings == 1.5.1'
    ],

    author='Chris Trotman',
    author_email='chris+gmrh@trotman.io',
    description='Easy tool for managing multiple git repositories.',
    license="BSD",
)
