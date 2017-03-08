import os
import re
import sys
import json
import platform
import datetime

import requests

from nukeuuid import get_nodes, set_uuid, NukeUUIDError


def import_nuke():
    try:
        import nuke
        return nuke
    except ImportError as e:
        try:
            os.environ['NON_PRODUCTION_CONTEXT']
        except KeyError:
            raise e


try:
    os.environ['NON_PRODUCTION_CONTEXT']
except:
    if platform.system() == 'Darwin':
        application = r'Nuke\d+\.\d+v\d+.app'
    elif platform.system() == 'Windows':
        application = r'Nuke\d+\.\d+.exe'
    else:
        raise RuntimeError('OS {0} is not supported'.format(platform.system()))
    match = re.search(application, sys.executable)
    if not match:
        raise RuntimeError('Import nukedatastore from within Nuke')
    nuke = import_nuke()

__version__ = '0.1.1'
__all__ = []

DS_PREFIX = 'ds_'
FROZEN_ATTR = 'nds_frozen'


class NukeDataStoreError(ValueError):
    """
    Exception indicating an error related to the Nuke Data Store,
    inherits from :class:`ValueError`.
    """
    def __init__(self, message):
        super(NukeDataStoreError, self).__init__(message)


class NukeDataStore(object):
    """
    NukeDataStore class, wrapper around Nuke's NoOp node.

    :param name: Data store name
    :type name: str

    Usage:

    >>> from nukedatastore import NukeDataStore
    >>> ds = NukeDataStore('data_store')
    >>> ds['project_data'] = {'id': 1234, 'name': 'project name'}
    >>> print ds['project_data']
    >>> {'id': 1234, 'name': 'project name'}
    """
    def __init__(self, name):
        self.store = self._init(name)

    @property
    def store(self):
        """
        Return the data store's Nuke node

        :return: Data store node
        :rtype: :class:`~nuke.Node`
        """
        try:
            assert self._store
        except (AssertionError, ValueError):
            raise NukeDataStoreError('Data store node missing')
        return self._store

    @store.setter
    def store(self, node):
        """
        Given a ``node``, set the ``store`` property. Raise
        :class:`~nukedatastore.NukeDataStoreError` if ``node`` has an
        incorrect type.

        :param node: Nuke node
        :type node: :class:`~nuke.Node`
        """
        if not isinstance(node, nuke.Node):
            raise NukeDataStoreError('Data store must be a Nuke node')
        self._store = node

    def _init(self, name):
        """
        Given a ``name``, initialise a :class:`~nukedatastore.NukeDataStore`
        with the same ``name``. Find existing
        :class:`~nukedatastore.NukeDataStore` nodes or create a new node with
        the same ``name``.

        :param node: Node name
        :type node: str
        :return: Data store node
        :rtype: :class:`~nuke.Node`
        """
        kw = {'': '356455a5-3e58-47b7-8d37-3bb37610187b'}
        attrs = {
            'label': 'NukeDataStore',
            'hide_input': True,
            'tile_color': 4278190335,
            FROZEN_ATTR: self._to_json(False)
        }
        store = None
        try:
            nodes = get_nodes(**kw)
            for node in nodes:
                if node.name() == name:
                    store = node
            assert store
        except (AssertionError, NukeUUIDError):
            store = nuke.nodes.NoOp(name=name)
            set_uuid(store, **kw)
            store.addKnob(self._create_knob(FROZEN_ATTR))
        for attr, value in attrs.iteritems():
            store[attr].setValue(value)
        return store

    def _create_knob(self, attr):
        """
        Given an ``attr``, create and return a new :class:`~nuke.Text_Knob` of
        the same name.

        :param attr: Attribute name
        :type attr: str
        :return: Nuke text knob
        :rtype: :class:`~nuke.Text_Knob`
        """
        knob = nuke.Text_Knob(attr, attr)
        knob.setEnabled(False)
        knob.setVisible(False)
        return knob

    def _get_ds_attr(self, key):
        """
        Given a ``key``, prefix with the data store prefix and return.

        :param key: Data store key
        :type key: str
        :return: Prefixed data store key
        :rtype: str
        """
        return '{ds_prefix}{key}'.format(ds_prefix=DS_PREFIX, key=key)

    def _strip_ds_attr(self, key):
        """
        Given a ``key``, remove the data store prefix and return.

        :param key: Prefixed data store key
        :type key: str
        :return: Data store key
        :rtype: str
        """
        return key[len(DS_PREFIX):]

    def _to_json(self, value):
        """
        Given a ``value``, encode to JSON and return.

        :param value: Decoded value
        :type value: str
        :return: JSON-encoded value
        :rtype: str
        """
        return json.dumps(value)

    def _from_json(self, value):
        """
        Given a ``value``, decode from JSON and return.

        :param value: JSON-encoded value
        :type value: str
        :return: Decoded value
        :rtype: str
        """
        return json.loads(value)

    def __getitem__(self, key):
        try:
            return self._get_item(key)
        except KeyError as e:
            raise KeyError(e)

    def _get_item(self, key, ds_attr=True):
        """
        Given a ``key`` get data attribute ``key``. Raise :class:`KeyError`, if
        key does not exist.

        :param key: Data store key
        :type key: str
        :param ds_attr: Prefix ``key`` with DS_PREFIX
        :type ds_attr: bool
        """
        try:
            if ds_attr:
                return self._from_json(
                    self.store[self._get_ds_attr(key)].value())
            else:
                return self._from_json(self.store[key].value())
        except NameError:
            raise KeyError(key)

    def _check_frozen(self):
        """
        Check if instance is frozen and raise
        :class:`~nukedatastore.NukeDataStoreError` if frozen.
        """
        if self.is_frozen():
            raise NukeDataStoreError('Cannot mutate frozen {0}'.format(
                self.__class__.__name__))

    def __setitem__(self, key, value):
        self._check_frozen()
        self._set_item(key, value)

    def _set_item(self, key, value, ds_attr=True):
        """
        Given a ``key``, ``value`` pair, set ``value`` on attribute ``key``.
        Raise :class:`~nukedatastore.NukeDataStoreError` is data is not JSON
        serialisable.

        :param key: Data store key
        :type key: str
        :param value: Data
        :type value: str, int, float, bool, list, dict
        :param ds_attr: Prefix ``key`` with DS_PREFIX
        :type ds_attr: bool
        """
        if ds_attr:
            key = self._get_ds_attr(key)
        try:
            serialised_data = self._to_json(value)
        except TypeError:
            raise NukeDataStoreError('Data not serialisable')
        try:
            self.store[key].setValue(serialised_data)
        except NameError:
            self.store.addKnob(self._create_knob(key))
            self.store[key].setValue(serialised_data)

    def list(self):
        """
        List all available keys in the :class:`~nukedatastore.NukeDataStore`.
        """
        return [self._strip_ds_attr(key) for key in self.store.knobs()
                if key.startswith(DS_PREFIX)]

    def is_frozen(self):
        """
        Return whether the data in the :class:`~nukedatastore.NukeDataStore`
        is frozen and therefore unchangeable.
        """
        return self._get_item(FROZEN_ATTR, ds_attr=False)

    def freeze(self):
        """
        Freeze the data in the :class:`~nukedatastore.NukeDataStore` and make
        it unchangeable.
        """
        self._set_item(FROZEN_ATTR, True, ds_attr=False)

    def unfreeze(self):
        """
        Unfreeze the data in the :class:`~nukedatastore.NukeDataStore` and
        make it changeable.
        """
        self._set_item(FROZEN_ATTR, False, ds_attr=False)

    def __repr__(self):
        return '<NukeDataStore: {0}, Keys: {1}>'.format(self.store.name(),
                                                        len(self.list()))


class NukeAPICache(NukeDataStore):
    """
    NukeAPICache class, inherits from :class:`~nukedatastore.NukeDataStore`.

    :param name: Data store name
    :type name: str

    Usage:

    >>> from nukedatastore import NukeAPICache
    >>> api_cache = NukeAPICache('api_cache')
    >>> api_cache.register('project_data', 'https://project.your.domain.com/api')
    >>> print api_cache['project_data']
    >>> {'id': 1234, 'name': 'project name'}
    """
    def __init__(self, name):
        super(NukeAPICache, self).__init__(name)

    def __setitem__(self, key, value):
        raise NotImplementedError('Please update API cache instead of trying '
                                  'to set the data manually, use '
                                  'NukeDataStore as a generic data store')

    def _check_exists(self, name):
        """
        Check if API is already registered on the instance, raise
        :class:`~nukedatastore.NukeDataStoreError` if registered.
        """
        try:
            self._get_api(name)
            raise NukeDataStoreError('API {0} already registered'.format(name))
        except KeyError:
            pass

    def register(self, name, url, update=True, ignore_exists=True):
        """
        Given a ``name`` and a ``url``, register a new API in the cache.

        :param name: API name
        :type name: str
        :param url: API URL
        :type url: str
        :param update: Update API data after registering, default: ``True``
        :type update: bool
        :param ignore_exists: Ignore API is already registered, default: ``True``
        :type ignore_exists: bool
        """
        self._check_frozen()
        if not ignore_exists:
            self._check_exists(name)
        self._set_item(name, [url, None, None])
        if update:
            self.update(name)

    def timestamp(self, *args):
        """
        Given \*args, return timestamps for specified APIs, if no APIs are
        specified, return timestamps for all registered APIs.

        :param \*args: API names
        :type \*args: str
        :return: List of timestamp tuples (api_name, timestamp)
        :rtype: list
        """
        if not args:
            args = self.list()
        response = []
        for api_name in args:
            response.append((api_name, self._get_api(api_name)[1]))
        return response

    def update(self, *args):
        """
        Given \*args, update specified APIs, if no APIs are specified, update
        all registered APIs.

        :param \*args: API names
        :type \*args: str
        """
        self._check_frozen()
        if not args:
            args = self.list()
        for api_name in args:
            url = self._get_api(api_name)[0]
            request = requests.get(url)
            try:
                request.raise_for_status()
            except requests.RequestException:
                raise NukeDataStoreError('Updating {0} failed'.format(
                    api_name))
            self._set_item(api_name, [url,
                                      datetime.datetime.utcnow().isoformat(),
                                      request.json()])

    def _get_api(self, key):
        """
        Given a ``key`` get API data for ``key``. Raise :class:`KeyError`, if
        key does not exist.

        :param key: Data store key
        :type key: str
        :param ds_attr: Prefix ``key`` with DS_PREFIX
        :type ds_attr: bool

        API format:

        >>> [url, timestamp, data]
        """
        try:
            return self._from_json(
                self.store[self._get_ds_attr(key)].value())
        except NameError:
            raise KeyError(key)

    def _get_item(self, key, ds_attr=True):
        """
        Given a ``key`` get data attribute ``key``. Raise :class:`KeyError`, if
        key does not exist.

        :param key: Data store key
        :type key: str
        :param ds_attr: Prefix ``key`` with DS_PREFIX
        :type ds_attr: bool
        """
        try:
            if ds_attr:
                return self._from_json(
                    self.store[self._get_ds_attr(key)].value())[-1]
            else:
                return self._from_json(self.store[key].value())
        except NameError:
            raise KeyError(key)

    def __repr__(self):
        return '<NukeAPICache: {0}, APIs: {1}>'.format(self.store.name(),
                                                       len(self.list()))
