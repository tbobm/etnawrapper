#!/usr/bin/env python3
# coding: utf-8
"""
Wrapper for ETNA's APIs

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
    """
    Happens when the API stops responding
    """
    pass


class BadStatusException(Exception):
    """
    The API responded with an unexpected status code
    """
    def __init__(self, message):
        self.message = message
        super(BadStatusException, self).__init__(message)


class EtnaWrapper(object):

    """Docstring for EtnaWrapper. """

    def __init__(self, **kwargs):
        """Initialises the EtnaWrapper. Gets a cookie.

        :param str login: Login of the user
        :param str password: Password of the user
        :param int retries: Number of time to retry while requesting a cookie

        """
        self._login = kwargs.get('login', None)
        password = kwargs.get('password', None)
        self._retries = kwargs.get('retries', 5)
        self._cookie = kwargs.get('cookies', None)
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
        """
        Wraps the calls the url, with the given arguments

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
        """
        GET Infos about the user

        :return: JSON
        """
        return self._request_api(url=IDENTITY_URL).json()

    def get_infos_with_id(self, logid):
        """
        GET Infos about a user given its id

        :return: JSON
        """
        _logid = logid
        _user_info_url = USER_INFO_URL.format(logid=_logid)
        return self._request_api(url=_user_info_url).json()

    def get_promos(self):
        """
        GET Promos of user

        :return: JSON
        """
        return self._request_api(url=USER_PROMO_URL).json()

    def get_current_activities(self, **kwargs):
        """
        GET Current activities of user

        :return: JSON
        """
        _login = kwargs.get('login', self._login)
        _activity_url = ACTIVITY_URL.format(login=_login)
        return self._request_api(url=_activity_url).json()

    def get_notifications(self, **kwargs):
        """
        GET Notifications of user

        :return: JSON
        """
        _login = kwargs.get('login', self._login)
        _notif_url = NOTIF_URL.format(login=_login)
        return self._request_api(url=_notif_url).json()

    def get_grades(self, **kwargs):
        """
        GET User's grades

        :return: JSON
        """
        _login = kwargs.get('login', self._login)
        _promotion_id = kwargs.get('promotion')
        _grades_url = GRADES_URL.format(login=_login, promo_id=_promotion_id)
        return self._request_api(url=_grades_url).json()

    def get_picture(self, **kwargs):
        """
        GET A user's picture

        :param str login: Login of the user to check
        :return: JSON
        """
        _login = kwargs.get('login', self._login)
        _activities_url = PICTURE_URL.format(login=_login)
        return self._request_api(url=_activities_url).content

    def get_projects(self, **kwargs):
        """
        GET User's project

        :param str login: User's login (Default: self._login)
        :return: JSON
        """
        _login = kwargs.get('login', self._login)
        search_url = SEARCH_URL.format(login=_login)
        return self._request_api(url=search_url).json()

    def get_activities_for_project(self, **kwargs):
        """
        GET Current activities of user

        :param str module: Stages of a given module
        :return: JSON
        """
        _module_id = kwargs.get('module')
        _activities_url = ACTIVITIES_URL.format(module_id=_module_id)
        return self._request_api(url=_activities_url).json()

    def get_group_for_activity(self, **kwargs):
        """
        GET groups for activity

        :param str module: Base module
        :param str module: Project which contains the group requested
        :return: JSON
        """
        _module_id = kwargs.get('module')
        _project_id = kwargs.get('project')
        _url = GROUPS_URL.format(module_id=_module_id, project_id=_project_id)
        return self._request_api(url=_url).json()

    def get_students(self, **kwargs):
        """
        GET users by promotion id

        :param int promotion: Promotion ID
        :return: JSON
        """
        _promotion_id = kwargs.get('promotion')
        _url = PROMOTION_URL.format(promo_id=_promotion_id)
        return self._request_api(url=_url).json()

__all__ = [
    'BadStatusException',
    'EtnaWrapper',
    'MaxRetryError',
]
