Getting Started
===============

To get started with ``nukedatastore``, type in the Nuke Script Editor:

.. code-block:: python

    import nukedatastore

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
