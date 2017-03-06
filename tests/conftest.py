# nukedatastore py.test configuration
import pytest
from nukedatastore import NukeDataStore


@pytest.fixture(scope='session')
def datastore():
    return NukeDataStore('data_store')


@pytest.fixture(scope='session')
def nuke():
    import nuke
    return nuke
