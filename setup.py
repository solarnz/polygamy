#!/usr/bin/env python

from setuptools import setup

setup(
    name='polygamy',
    version='0.1.1-dev',
    packages=['polygamy'],
    entry_points={
        'console_scripts': [
            'polygamy = polygamy:main'
        ]
    },
    install_requires=[
        'blessings == 1.5.1',
        'tabulate == 0.7.2',
    ],

    author='Chris Trotman',
    author_email='chris+poly@trotman.io',
    description='Easy tool for managing multiple git repositories.',
    license="BSD",
)
