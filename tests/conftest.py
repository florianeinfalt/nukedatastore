# nukedatastore py.test configuration
import pytest
from nukedatastore import NukeDataStore, NukeAPICache


@pytest.fixture(scope='session')
def datastore():
    return NukeDataStore('data_store')


@pytest.fixture(scope='session')
def api_cache():
    return NukeAPICache('api_cache')


@pytest.fixture(scope='session')
def nuke():
    import nuke
    return nuke
