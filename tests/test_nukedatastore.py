# nukedatastore tests
import pytest
import datetime

from nukedatastore import NukeDataStore, NukeDataStoreError


def test_datastore_crud(datastore):
    datastore['project_data'] = {'id': 1234, 'name': 'project name'}
    assert len(datastore.list()) == 1
    assert datastore.list()[0] == 'project_data'
    assert datastore['project_data'] == {'id': 1234, 'name': 'project name'}


def test_datastore_crud_invalid_key(datastore):
    with pytest.raises(KeyError):
        datastore['invalid_key']


def test_datastore_crud_invalid_data(datastore):
    with pytest.raises(NukeDataStoreError):
        datastore['data'] = datetime.datetime.now()


def test_datastore_crud_frozen(datastore):
    datastore.freeze()
    with pytest.raises(NukeDataStoreError):
        datastore['project_data'] = {}
    datastore.unfreeze()


def test_deleted_node(datastore, nuke):
    nuke.delete(nuke.toNode('data_store'))
    with pytest.raises(NukeDataStoreError):
        datastore.store


def test_existing_node_init(nuke):
    NukeDataStore('data_store')
    x = NukeDataStore('data_store')
    assert x
