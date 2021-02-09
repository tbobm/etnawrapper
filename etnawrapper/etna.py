#!/usr/bin/env python3
"""Client for ETNA's APIs"""
# TODO: Implement a Session upon instantiation?
# TODO: Cli ? :o
# TODO: CLI.
from datetime import datetime
from typing import Union, List
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
    DECLARATIONS_URL,
    CONVERSATIONS_URL,
    TICKET_URL,
    TICKETS_URL,
)


__author__ = "Theo Massard <massar_t@etna-alternance.net>"


class EtnaWrapper:
    """"""

    def __init__(
        self,
        login: str = None,
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
        self, url: str, method="GET", raw: bool = False, data=None, params=None,
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
            params=params,
            headers=self.headers,
            timeout=50,
        )
        if raw:
            return response  # type: requests.Response
        return response.json()  # type: dict

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

    def get_user_promotion(self, login: str = None) -> dict:
        """Return user's promotions."""
        url = USER_PROMO_URL
        if login is not None:
            url = USER_PROMO_URL + "?login=" + login

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

    def get_projects(self, login: str = None, date: datetime = None) -> dict:
        """Fetch a student's projects base on the login."""
        url = SEARCH_URL.format(login=login or self.login)
        params = dict()
        if date is not None:
            _date = date.strftime('%Y-%m-%d')
            params["date"] = _date
        result = self._query(url, params=params)
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

    def get_conversations(self, user_id: int, start: int = None, size: int = None) -> dict:
        """Return the list of conversations for a user.

        Requires read permission for this user_id.
        Use this method with a user_id corresponding to your login
        to ensure readability.
        """
        url = CONVERSATIONS_URL.format(user_id=user_id)
        params = dict()
        if start is not None:
            params['from'] = start
        if size is not None:
            params['size'] = size
        result = self._query(url, params=params)
        return result

    def get_declarations(self, start: str = None, end: str = None) -> dict:
        """Return the list of declarations for a user.

        Requires read permission for this login.
        """
        url = DECLARATIONS_URL.format(login=self.login)
        params = dict()
        if start is not None:
            params['start'] = start
        if end is not None:
            params['end'] = end
        result = self._query(url, params=params)
        return result

    def declare_log(self, module_id: int, content: dict):
        """Send a log declaration for module_id with `content`.

        Content should be of the following form:

        >>> content = {
                "module": 1111,
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
        )
        result = self._query(url, method='OPTIONS', raw=True)
        result = self._query(url, method='POST', data=content)
        return result

    def open_ticket(self, title: str, message: str, tags: List[str] = None, users: List[str] = None):
        """Open a ticket."""
        content = {}
        content['title'] = title
        content['message'] = message
        content['tags'] = tags
        content['users'] = users

        url = TICKETS_URL
        result = self._query(url, method='OPTIONS', raw=True)
        result = self._query(url, method='POST', data=content)

        return result

    def close_ticket(self, ticket_id: int):
        """Close a ticket."""
        url = TICKET_URL.format(task_id=ticket_id)
        result = self._query(url, method='DELETE')
        return result

    def get_tickets(self):
        """Fetch the list of tickets."""
        url = TICKETS_URL
        result = self._query(url)
        return result
    
    
    def get_ticket(self, ticket_id: int):
        """Fetch the ticket matching `ticket_id`."""
        url = TICKET_URL.format(task_id=ticket_id)
        result = self._query(url)
        return result


__all__ = ("EtnaWrapper",)
