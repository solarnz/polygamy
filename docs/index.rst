.. Polygamy documentation master file, created by
   sphinx-quickstart on Mon Mar 24 21:14:44 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Polygamy's documentation!
====================================

Contents:

.. toctree::
   :maxdepth: 2


Introduction
============

What is polygamy? Isn't that illegal? Well, in some countries yes. Polygamy is
a tool for handling multiple git repositories. It is in part inspired by `repo`
by Google, however that only really works well when used with Gerrit.

Installation
============

You can currently only install the git version of polygamy. As progress is
made, releases will be uploaded to pypi, where it will be easier for you to
install.

Development Version
-------------------
.. code-block:: shell

    pip install git+https://github.com/solarnz/polygamy

Configuration
=============

Currently the recommended way to setup polygamy is to create a `.polygamy`
directory, containing a file called `polygamy.json`. Within this json file, all
of the remotes and all of the repositories are configured.

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
                "name": "/solarnz/molokai",
                "remote": "github",
            },
            "toast": {
                "name": "/solarnz/toast"
            },
            "bread": {
                "name": "/solarnz/bread"
            }
        }
    }

The configuration is mostly self explanatory, however it is important to note
that at this stage, a repository can only have one remote.

If there is only one remote setup, then there is no need to specify which
remote to use in each repository, as it will default to the only remote.
Likewise, you can explicitly define the default remote by setting `default` to
`true`.

There is currently no support for defining multiple remotes within a
repository, however that will be implemented in the near future.

Also note that within development, the configuration format may change without
warning.

Usage
=====

init
----

.. code-block:: shell

    polygamy init git://github.com/solarnz/polygamy_config

status
------

.. code-block:: shell

    polygamy status

fetch
-----

.. code-block:: shell

    polygamy fetch

pull
----

.. code-block:: shell

    polygamy pull

list
----

.. code-block:: shell

    polygamy list

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

