===============================
polygamy
===============================

.. image:: https://badge.fury.io/py/polygamy.png
    :target: http://badge.fury.io/py/polygamy
    
.. image:: https://travis-ci.org/solarnz/polygamy.png?branch=master
        :target: https://travis-ci.org/solarnz/polygamy

.. image:: https://pypip.in/d/polygamy/badge.png
        :target: https://pypi.python.org/pypi/polygamy


Handle multiple SCM repositories easily.

* Free software: BSD license
* Documentation: http://polygamy.readthedocs.org.

Features
--------

* TODO


Installation
------------

.. code-block:: bash

    pip install git+https://github.com/solarnz/polygamy

Configuration
-------------

.. code-block:: json
    {
        "remotes": {
            "github": {
                "url": "git@github.com:",
                "branch": "master"
            }
        },
        "repos": {
            "molokai": {
                "remote": "github",
                "name": "/solarnz/molokai"
            }
        }
    }

Usage
-----
`polygamy` in the same directory that the .polygamy.json file is in.
