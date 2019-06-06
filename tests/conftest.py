import responses
import pytest

from etnawrapper import etna, constants


@pytest.fixture(scope='session')
def login():
    return 'test_u'


@responses.activate
@pytest.fixture(scope='session')
def client():
    responses.add(responses.POST, constants.AUTH_URL)
    return etna.EtnaWrapper('test_u', 'password')
