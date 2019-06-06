import pytest
import requests
import responses

from etnawrapper import etna, constants


@responses.activate
def test_wrapper_class():
    responses.add(responses.POST, constants.AUTH_URL)
    client = etna.EtnaWrapper("test_u", "password")
    assert client is not None
    assert isinstance(client._req, type(requests))

    client = etna.EtnaWrapper("test_u", "password", use_session=True)
    assert client is not None
    assert isinstance(client._req, requests.Session)

    # display
    _s = str(client)
    assert _s == "<etnawrapper.etna.EtnaWrapper(login='test_u', cookies={})>"

    # missing password
    with pytest.raises(ValueError):
        etna.EtnaWrapper("sample", None)

    # missing login
    with pytest.raises(ValueError):
        etna.EtnaWrapper(None)

    # cookie creation
    cookie_based = etna.EtnaWrapper("test_u", cookies={"jwt": "abcdef"})
    assert cookie_based is not None

    # equality
    assert client != cookie_based
    assert client == client
    with pytest.raises(NotImplementedError):
        client == 42


@responses.activate
def test_declaration(client: etna.EtnaWrapper, login: str):
    m_id, a_id = 18, 22
    start, end = '2019-05-6 9:00', '2019-05-6 9:00'
    content = {
        'module': m_id,
        'activity': a_id,
        'declaration': {
            'start': start,
            'end': end,
            'content': 'asdf\nfdsa',
        },
    }
    url = constants.DECLARATION_URL.format(login=login, module_id=m_id, activity_id=a_id)
    responses.add(responses.POST, url, json={'declared': True})
    result = client.declare_log(m_id, a_id, content)
    assert result['declared']
