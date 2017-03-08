# nukeapi_cache tests
import pytest
import datetime

from nukedatastore import NukeAPICache, NukeDataStoreError


def test_api_cache_set_invalid(api_cache):
    with pytest.raises(NotImplementedError):
        api_cache['project_data'] = 123

def test_api_cache_register(api_cache):
    api_cache.register('project_data',
                       'https://httpbin.org/get',
                       ignore_exists=False)
    assert len(api_cache.list()) == 1
    assert api_cache.list()[0] == 'project_data'
    assert api_cache['project_data']['url'] == 'https://httpbin.org/get'


def test_api_cache_register_exists_invalid(api_cache):
    with pytest.raises(NukeDataStoreError):
        api_cache.register('project_data',
                           'https://httpbin.org/get',
                           ignore_exists=False)

def _convert_iso_to_dt(timestamp):
    try:
        return datetime.datetime.strptime(timestamp,
                                          '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        return datetime.datetime.strptime(timestamp,
                                          '%Y-%m-%dT%H:%M:%S')

def test_api_cache_update(api_cache):
    before = _convert_iso_to_dt(api_cache.timestamp('project_data')[0][1])
    api_cache.update()
    after = _convert_iso_to_dt(api_cache.timestamp('project_data')[0][1])
    assert after > before


def test_api_cache_update_invalid(api_cache):
    temp_cache = NukeAPICache('temp_cache')
    temp_cache.register('invalid_api', 'https://httpbin.org/get2',
                        update=False)
    with pytest.raises(NukeDataStoreError):
        temp_cache.update()


def test_api_cache_timestamps(api_cache):
    assert len(api_cache.timestamp()) == 1


def test_api_cache_crud_frozen(api_cache):
    api_cache.freeze()
    with pytest.raises(NukeDataStoreError):
        api_cache.update()
    api_cache.unfreeze()
