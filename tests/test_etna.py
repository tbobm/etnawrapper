import responses

from etnawrapper import etna, constants


@responses.activate
def test_wrapper_creation():
    responses.add(responses.POST, constants.AUTH_URL)
    client = etna.EtnaWrapper('test_u', 'password')
    assert client is not None
