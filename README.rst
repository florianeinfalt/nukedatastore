nukedatastore
=============

.. image:: https://img.shields.io/pypi/l/nukedatastore.svg
    :target: https://pypi.python.org/pypi/nukedatastore
.. image:: https://img.shields.io/pypi/pyversions/nukedatastore.svg
    :target: https://pypi.python.org/pypi/nukedatastore
.. image:: https://img.shields.io/pypi/v/nukedatastore.svg
    :target: https://pypi.python.org/pypi/nukedatastore
.. image:: https://img.shields.io/pypi/wheel/nukedatastore.svg
    :target: https://pypi.python.org/pypi/nukedatastore
.. image:: https://readthedocs.org/projects/nukedatastore/badge/?version=latest
    :target: https://readthedocs.org/projects/nukedatastore/?badge=latest

A library for basic data persistence in Nuke

`Full Documentation`_

Installation
------------

To install ``nukedatastore``, type:

.. code-block:: bash

    $ pip install nukedatastore

Open Nuke's ``init.py`` file and add:

.. code-block:: python

    nuke.pluginAddPath('/path/to/your/local/python/site-packages')

Getting Started
---------------

To get started with ``nukedatastore``, type in the Nuke Script Editor:

.. code-block:: python

    import nukedatastore

NukeDataStore
~~~~~~~~~~~~~

To initialise a ``NukeDataStore``, type:

.. code-block:: python

    ds = nukedatastore.NukeDataStore('data_store')

To store data in the ``NukeDataStore``, type:

.. code-block:: python

    ds['project_data'] = {'id': 1234, 'name': 'project name'}

To list all available keys in the ``NukeDataStore``, type:

.. code-block:: python

    ds.list()
    # ['project_data']

To retrieve stored data from the ``NukeDataStore``, type:

.. code-block:: python

    ds['project_data']
    # {'id': 1234, 'name': 'project name'}

A ``NukeDataStore`` can be frozen, to freeze, type:

.. code-block:: python

    ds.freeze()

Any further attempt to set data on the ``NukeDataStore`` will result in
an error:

.. code-block:: python

    ds['color_data'] = {'id': 'AB-123', 'name': 'White'}
    # nukedatastore.NukeDataStoreError: Cannot mutate frozen NukeDataStore

To un-freeze, type:

.. code-block:: python

    ds.unfreeze()

NukeAPICache
~~~~~~~~~~~~

Working with the ``NukeAPICache`` is very similar. To register an API, type:

.. code-block:: python

    api_cache = nukedatastore.NukeAPICache('api_cache')
    api.cache.register('project_data', 'https://project.your.domain.com')

To read the cached API data, type:

.. code-block:: python

    api_cache['project_data']

To update the API data, type:

.. code-block:: python

    api_cache.update('project_data')

.. _Full Documentation: http://nukedatastore.readthedocs.io/en/latest/
