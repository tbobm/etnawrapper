#!/usr/bin/env python3
"""Client for ETNA's APIs"""
# TODO: Implement a Session upon instantiation?
# TODO: Cli ? :o
# TODO: CLI.
from datetime import datetime
from typing import Union
from io import BytesIO

import requests

from .constants import (
    AUTH_URL,
    IDENTITY_URL,
    USER_INFO_URL,
    PROMOTION_URL,
    USER_PROMO_URL,
    ACTIVITY_URL,
    NOTIF_URL,
    GRADES_URL,
    PICTURE_URL,
    SEARCH_URL,
    ACTIVITIES_URL,
    GROUPS_URL,
    GSA_EVENTS_URL,
    GSA_LOGS_URL,
    EVENTS_URL,
    DECLARATION_URL,
)


__author__ = "Theo Massard <massar_t@etna-alternance.net>"


class EtnaWrapper:
    """"""

    def __init__(
        self,
        login: str,
        password: str = None,
        cookies: dict = None,
        use_session: bool = False,
        headers: dict = None,
    ):
        self.login = login
        self._cookies = cookies
        if cookies is None:
            self._cookies = self.get_cookies(login, password)
        # XXX: be careful about this one
        if use_session:
            self._req = requests.Session()
        else:
            self._req = requests
        self.headers = headers

    def __repr__(self):
        return "<etnawrapper.etna.EtnaWrapper(login='{}', cookies={})>".format(
            self.login, self._cookies
        )

    def __eq__(self, obj):
        if not isinstance(obj, EtnaWrapper):
            raise NotImplementedError
        return (
            self.login == obj.login
            and self._cookies == obj._cookies
            and isinstance(self._req, type(obj._req))
        )

    def __neq__(self, obj):
        return not self == obj

    def _query(
        self, url: str, method="GET", raw: bool = False, data=None
    ) -> Union[dict, requests.Response]:
        """Perform a request using the `self._req` HTTP client.

        Upon requesting a non-standard URL (not returning JSON),
        the `raw` flag allow to return a `requests.Response` object
        instead of a dictionnary.
        """
        response = self._req.request(
            method,
            url,
            cookies=self._cookies,
            json=data,
            headers=self.headers,
            timeout=50,
        )
        if raw:
            return response
        return response.json()

    @staticmethod
    def get_cookies(login: str = None, password: str = None) -> str:
        """Fetch a Cookie."""
        if login is None:
            raise ValueError("missing login, can not authenticate")
        if password is None:
            raise ValueError("missing password, can not authenticate")
        data = {"login": login, "password": password}
        resp = requests.post(AUTH_URL, data=data)
        return resp.cookies.get_dict()

    def get_user_info(self, user_id: int = None) -> dict:
        """Return a user's informations. Defaults to self.login."""
        # TODO: Docstring -> show example
        url = IDENTITY_URL
        if user_id is not None:
            url = USER_INFO_URL.format(user_id=user_id)
        result = self._query(url)
        return result

    def get_promotion(self, promotion_id: int = None) -> dict:
        """Return a user's informations. Defaults to self.login."""
        # TODO: Docstring -> show example
        # NOTE: Is it actually the same output?
        url = USER_PROMO_URL
        if promotion_id is not None:
            url = PROMOTION_URL.format(promo_id=promotion_id)
        result = self._query(url)
        return result

    def get_current_activities(self, login: str = None) -> dict:
        """Return a user's current activities.

        Defaults to self.login.

        """
        url = ACTIVITY_URL.format(login=login or self.login)
        result = self._query(url)
        return result

    def get_notifications(self, login: str = None) -> dict:
        """Return `login`'s notifications.

        If login is not set, defaults to self.login.
        """
        url = NOTIF_URL.format(login=login or self.login)
        result = self._query(url)
        return result

    def get_grades(self, promotion_id: int, login: str = None) -> dict:
        """Fetch a student's grades, based on the promotion."""
        url = GRADES_URL.format(login=login or self.login, promo_id=promotion_id)
        result = self._query(url)
        return result

    def get_picture(self, login: str = None) -> BytesIO:
        url = PICTURE_URL.format(login=login or self.login)
        result = self._query(url, raw=True)
        return result.content

    def get_projects(self, login: str = None) -> dict:
        """Fetch a student's projects base on the login."""
        url = SEARCH_URL.format(login=login or self.login)
        result = self._query(url)
        return result

    def get_project_activites(self, module: str) -> dict:
        """Fetch activities related to `module`."""
        url = ACTIVITIES_URL.format(module_id=module)
        result = self._query(url)
        return result

    def get_group_for_activity(self, module: str, project: str) -> dict:
        """Return group composition for the module/project tuple."""
        url = GROUPS_URL.format(module_id=module, project_id=project)
        result = self._query(url)
        return result

    def get_students(self, promotion_id: int) -> dict:
        """Fetch every student bsaed on `promotion_id`."""
        url = PROMOTION_URL.format(promo_id=promotion_id)
        result = self._query(url)
        return result

    def get_log_events(self, login: str = None) -> dict:
        """Get a user's log event, defaults to self.login."""
        url = GSA_EVENTS_URL.format(login=login or self.login)
        result = self._query(url)
        return result

    def get_logs(self, login: str = None) -> dict:
        """Fetch a user's logs, defaults to self.login."""
        url = GSA_LOGS_URL.format(login=login or self.login)
        result = self._query(url)
        return result

    def get_events(
        self, start_date: datetime, end_date: datetime, login: str = None
    ) -> dict:
        """Fetch a user's events, defaults to self.login."""
        url = EVENTS_URL.format(
            login=login or self.login,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
        )
        result = self._query(url)
        return result

    def declare_log(self, module_id: int, activity_id: int, content: dict):
        """Send a log declaration for module_id/activity_id with `data`.

        Content should be of the following form:

        >>> content = {
                "module": 1111,
                "activity": 22222,
                "declaration": {
                    "start": "2019-05-6 10:00",
                    "end": "2019-05-6 10:00",
                    "content": "Objectifs: do things\n" \
                               "Actions: Did stuff\n" \
                               "Resultats: Got stuff done\n"
                },
            }
        """
        url = DECLARATION_URL.format(
            login=self.login,
            module_id=module_id,
            activity_id=activity_id,
        )
        print(content)
        result = self._query(url, method='POST', data=content)
        return result


__all__ = ("EtnaWrapper",)
