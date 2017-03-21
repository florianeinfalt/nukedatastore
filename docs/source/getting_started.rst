Getting Started
===============

To get started with ``nukedatastore``, type in the Nuke Script Editor:

.. code-block:: python

    import nukedatastore

NukeDataStore
-------------

To initialise a ``NukeDataStore``, type:

.. code-block:: python

    ds = nukedatastore.NukeDataStore('data_store')

.. note::

    ``nukedatastore`` will try to find an existing data store with the same
    name first, if that does not succeed, a new data store is created.

To store data in the ``NukeDataStore``, type:

.. code-block:: python

    ds['project_data'] = {'id': 1234, 'name': 'project name'}

.. note::

    If the key (i.e. ``project_data``) does not exists, then ``nukedatastore``
    will automatically create it.

.. warning::

    All data stored in ``NukeDataStore`` must be JSON serialisable.

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
------------

Working with the ``NukeAPICache`` is very similar. To register an API, type:

.. code-block:: python

    api_cache = nukedatastore.NukeAPICache('api_cache')
    api_cache.register('project_data', 'https://project.your.domain.com/api')

To read the cached API data, type:

.. code-block:: python

    api_cache['project_data']

To update the API data, type:

.. code-block:: python

    api_cache.update('project_data')

.. note::

    ``NukeAPICache`` supports freezing and unfreezing just like
    ``NukeDataStore``.

To diff existing API data with new API data, type:

.. code-block:: python

    api_cache.diff('project_data')
    # {'project_data': {'values_changed': {"root['headers']['X-Request-Id']": {'new_value': u'f5800c5e-4edb-4509-8339-4bcdf0b32732', 'old_value': u'd8ed6737-e5c8-49aa-b42e-58eb2ba472b9'}}}}
