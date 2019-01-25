#!/usr/bin/env python3
# coding: utf-8
"""Client for ETNA's APIs

Usage:
    >>> from etnawrapper import EtnaClient
    >>> client = EtnaClient(login='login', password='xxxxx')
    >>> client.get_infos()
    {
        "id": 0,
        "promotion": "promotion",
        # ...
    }

This usage is supposedly quite unsafe, mainly because you have to
type your password (which isn't stored in the EtnaClient object)
in clear text.
In order to avoid this, you can also login directly using a cookie.

Usage:
    >>> # same as above
    >>> client = EtnaClient(cookie='cookie-given-by-etna*')
    >>> client.get_infos()
    {
        # Same as above
    }

Upon client initialization, a call will be made to only store a cookie
in the object.

Based on https://github.com/josephbedminster/api-etna
"""
import logging
import yaml
import os

import requests

import constants


__author__ = 'Theo Massard <massar_t@etna-alternance.net>'

REQ = {
    'GET': requests.get,
    'POST': requests.post
}


logging.basicConfig(level=logging.DEBUG)

HERE = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(HERE, 'behaviours.yml')
CONFIG = yaml.load(open(CONFIG_PATH))


class MaxRetryError(Exception):
    """Happen when the API stops responding."""
    pass


class BadStatusException(Exception):
    """Receive unexpected reponse code."""

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class EtnaClient:
    """Simple HTTP client."""

    def __init__(
            self,
            login: str = None,
            password: str = None,
            cookie: str = None,
            retries: int = 5,
    ):
        """Initialise the EtnaClient.

        Make a call to AUTH_URL, store the login and dump the password away.
        Store a cookie.

        :param str login: Login of the user
        :param str password: Password of the user
        :param int retries: Number of time to retry while requesting a cookie
        """
        using_credentials = False
        using_cookie = False
        self.logger = logging.getLogger('etna-client')
        if cookie:
            using_cookie = True
            self._cookie = cookie
        if login and password:
            self.login = login
            using_credentials = True

        if not using_cookie and not using_credentials:
            raise ValueError('Provide either login/password or a cookie')

        if using_credentials:
            self.logger.debug('fetching cookie for %s', login)
            self._cookie = self._get_cookie(login=login, password=password)

        self._retries = retries
        self._last_result = None

    @classmethod
    def _get_cookie(cls, login: str = None, password: str = None):
        post_data = {
            'login': login,
            'password': password
        }
        print('fetching post')
        resp = requests.post(constants.AUTH_URL, json=post_data)
        print(resp)
        return resp.cookies.get_dict()

    def _request_api(self, url: str, method: str = 'GET', status: int = 200):
        """Wrap the calls the url, with the given arguments."""
        counter = 0
        if method not in ['GET', 'POST']:
            raise ValueError('method is not GET or POST')

        while True:
            try:
                res = REQ[method](url, cookies=self._cookie)
                if res.status_code == status:
                    break
                else:
                    raise BadStatusException(
                        'could not fetch url={} : {}'.format(
                            res.url,
                            res.text,
                        ),
                    )
            except requests.exceptions.BaseHTTPError:
                if counter < self._retries:
                    counter += 1
                    continue
                raise MaxRetryError
        self._last_result = res
        return res

    def f(self, name, **kwargs):
        try:
            entry = CONFIG.get(name)
            url = getattr(constants, entry['url'])
            method = entry.get('method', 'GET')
            post_process = entry.get('post_process')
            params = entry.get('params')
            if params:
                missings = set(params) ^ set(kwargs)
                print('missings', missings)
                for missing in missings:
                    kwargs[missing] = getattr(self, missing)
                url = url.format_map(kwargs)
            result = self._request_api(url, method)
            if post_process:
                fun = getattr(result, post_process)
                return fun() if callable(fun) else fun
            return result
        except KeyError:
            self.logger.exception('uh ohhh')
            raise NotImplementedError('could not reach {}'.format(name))


__all__ = (
    'BadStatusException',
    'EtnaClient',
    'MaxRetryError',
)
