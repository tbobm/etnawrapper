#!/usr/bin/env python3
# coding: utf-8
"""Client for ETNA's APIs

Usage:
    >>> from etnawrapper import EtnaWrapper
    >>> client = EtnaWrapper(login='login', password='xxxxx')
    >>> client.get_infos()
    {
        "id": 0,
        "promotion": "promotion",
        # ...
    }
    
This usage is supposedly quite unsafe, mainly because you have to
type your password (which isn't stored in the EtnaWrapper object)
in clear text.
In order to avoid this, you can also login directly using a cookie.

Usage:
    >>> # same as above
    >>> client = EtnaWrapper(cookie='cookie-given-by-etna*')
    >>> client.get_infos()
    {
        # Same as above
    }

Upon client initialization, a call will be made to only store a cookie
in the object.

Based on https://github.com/josephbedminster/api-etna
"""
import requests


__author__ = 'Theo Massard <massar_t@etna-alternance.net>'

PREP_API = 'https://prepintra-api.etna-alternance.net'
ETNA_API = 'https://auth.etna-alternance.net'
AUTH_URL = 'https://auth.etna-alternance.net/login'
MODULE_API = 'https://modules-api.etna-alternance.net'

IDENTITY_URL = ETNA_API + '/identity'
USER_INFO_URL = ETNA_API + '/api/users/{logid}'
USER_PROMO_URL = PREP_API + '/promo'
GRADES_URL = PREP_API + '/terms/{promo_id}/students/{login}/marks'
NOTIF_URL = PREP_API + '/students/{login}/informations'
ACTIVITY_URL = MODULE_API + '/students/{login}/currentactivities'
PICTURE_URL = ETNA_API + '/api/users/{login}/photo'
SEARCH_URL = MODULE_API + '/students/{login}/search'
ACTIVITIES_URL = MODULE_API + '/{module_id}/activities'
GROUPS_URL = PREP_API + '/sessions/{module_id}/project/{project_id}/groups'
PROMOTION_URL = PREP_API + '/trombi/{promo_id}'

REQ = {
    'GET': requests.get,
    'POST': requests.post
}


class MaxRetryError(Exception):
    """Happen when the API stops responding."""
    pass


class BadStatusException(Exception):
    """Receive unexpected reponse code."""
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class EtnaWrapper:
    """Simple HTTP client."""

    def __init__(
            self,
            login=None,
            password=None,
            cookie=None,
            **kwargs
        ):
        """Initialise the EtnaWrapper.

        Make a call to AUTH_URL, store the login and dump the password away.
        Store a cookie.

        :param str login: Login of the user
        :param str password: Password of the user
        :param int retries: Number of time to retry while requesting a cookie
        """

        self._login = kwargs.get('login', login)
        password = kwargs.get('password', password)
        self._retries = kwargs.get('retries', 5)
        self._cookie = kwargs.get('cookie', cookie)
        self._last_result = None

        ids = [self._login, password, self._cookie]
        if all(val is None for val in ids):
            raise ValueError('Provide either login/password, or a cookie')
        if self._cookie is None:
            self._get_cookie(password)

    def _get_cookie(self, password):
        post_data = {
            'login': self._login,
            'password': password
        }
        resp = requests.post(AUTH_URL, data=post_data)
        self._cookie = resp.cookies.get_dict()

    def _request_api(self, **kwargs):
        """Wrap the calls the url, with the given arguments.

        :param str url: Url to call with the given arguments
        :param str method: [POST | GET] Method to use on the request
        :param int status: Expected status code
        """
        _url = kwargs.get('url')
        _method = kwargs.get('method', 'GET')
        _status = kwargs.get('status', 200)

        counter = 0
        if _method not in ['GET', 'POST']:
            raise ValueError('Method is not GET or POST')

        while True:
            try:
                res = REQ[_method](_url, cookies=self._cookie)
                if res.status_code == _status:
                    break
                else:
                    raise BadStatusException(res.content)
            except requests.exceptions.BaseHTTPError:
                if counter < self._retries:
                    counter += 1
                    continue
                raise MaxRetryError
        self._last_result = res
        return res

    def get_infos(self):
        """Get info about the current user.

        :return: JSON
        """

        return self._request_api(url=IDENTITY_URL).json()

    def get_infos_with_id(self, uid):
        """Get info about a user based on his id.

        :return: JSON
        """

        _logid = uid
        _user_info_url = USER_INFO_URL.format(logid=_logid)
        return self._request_api(url=_user_info_url).json()

    def get_promos(self):
        """Get informations about the user's promotion.

        :return: JSON
        """

        return self._request_api(url=USER_PROMO_URL).json()

    def get_current_activities(self, login=None, **kwargs):
        """Get the current activities of user.

        Either use the `login` param, or the client's login if unset.
        :return: JSON
        """

        _login = kwargs.get(
            'login',
            login or self._login
        )
        _activity_url = ACTIVITY_URL.format(login=_login)
        return self._request_api(url=_activity_url).json()

    def get_notifications(self, login=None, **kwargs):
        """Get the current notifications of a user.

        :return: JSON
        """

        _login = kwargs.get(
            'login',
            login or self._login
        )
        _notif_url = NOTIF_URL.format(login=_login)
        return self._request_api(url=_notif_url).json()

    def get_grades(self, login=None, promotion=None, **kwargs):
        """Get a user's grades on a single promotion based on his login.

        Either use the `login` param, or the client's login if unset.
        :return: JSON
        """

        _login = kwargs.get(
            'login',
            login or self._login
        )
        _promotion_id = kwargs.get('promotion', promotion)
        _grades_url = GRADES_URL.format(login=_login, promo_id=_promotion_id)
        return self._request_api(url=_grades_url).json()

    def get_picture(self, login=None, **kwargs):
        """Get a user's picture.

        :param str login: Login of the user to check
        :return: JSON
        """

        _login = kwargs.get(
            'login',
            login or self._login
        )
        _activities_url = PICTURE_URL.format(login=_login)
        return self._request_api(url=_activities_url).content

    def get_projects(self, **kwargs):
        """Get a user's project.

        :param str login: User's login (Default: self._login)
        :return: JSON
        """

        _login = kwargs.get('login', self._login)
        search_url = SEARCH_URL.format(login=_login)
        return self._request_api(url=search_url).json()

    def get_activities_for_project(self, module=None, **kwargs):
        """Get the related activities of a project.

        :param str module: Stages of a given module
        :return: JSON
        """

        _module_id = kwargs.get('module', module)
        _activities_url = ACTIVITIES_URL.format(module_id=_module_id)
        return self._request_api(url=_activities_url).json()

    def get_group_for_activity(self, module=None, project=None, **kwargs):
        """Get groups for activity.

        :param str module: Base module
        :param str module: Project which contains the group requested
        :return: JSON
        """

        _module_id = kwargs.get('module', module)
        _project_id = kwargs.get('project', project)
        _url = GROUPS_URL.format(module_id=_module_id, project_id=_project_id)
        return self._request_api(url=_url).json()

    def get_students(self, **kwargs):
        """Get users by promotion id.

        :param int promotion: Promotion ID
        :return: JSON
        """

        _promotion_id = kwargs.get('promotion')
        _url = PROMOTION_URL.format(promo_id=_promotion_id)
        return self._request_api(url=_url).json()


__all__ = (
    'BadStatusException',
    'EtnaWrapper',
    'MaxRetryError',
)
