#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='polygamy',

    version='0.1.2',
    description='Handle multiple SCM repositories easily.',
    long_description=readme + '\n\n' + history,
    author='Chris Trotman',
    author_email='chris@trotman.io',
    url='https://github.com/solarnz/polygamy',
    packages=[
        'polygamy',
    ],
    include_package_data=True,
    install_requires=[
        'blessings == 1.5.1',
        'gevent >= 1.0',
        'tabulate == 0.7.2',
    ],
    license="BSD",
    zip_safe=False,
    keywords='polygamy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'polygamy = polygamy:main'
        ]
    },
)
