import pytest
import requests
import responses

from etnawrapper import etna, constants


@responses.activate
def test_wrapper_class():
    responses.add(responses.POST, constants.AUTH_URL)
    client = etna.EtnaWrapper('test_u', 'password')
    assert client is not None
    assert isinstance(client._req, type(requests))

    client = etna.EtnaWrapper('test_u', 'password', use_session=True)
    assert client is not None
    assert isinstance(client._req, requests.Session)

    # display
    _s = str(client)
    assert _s == "<etnawrapper.etna.EtnaWrapper(login='test_u', cookies={})>"

    # missing password
    with pytest.raises(ValueError):
        etna.EtnaWrapper('sample', None)

    # missing login
    with pytest.raises(ValueError):
        etna.EtnaWrapper(None)

    # cookie creation
    cookie_based = etna.EtnaWrapper('test_u', cookies={'jwt': 'abcdef'})
    assert cookie_based is not None

    # equality
    assert client != cookie_based
    assert client == client
    with pytest.raises(NotImplementedError):
        client == 42
