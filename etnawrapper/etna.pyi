"""
"""
import typing


class EtnaClient:
    def get_infos(self) -> dict:
        """Fetch user informations."""
        ...

    def get_infos_with_id(self, user_id: int) -> dict:
        """Fetch `user_id`'s informations.'"""
        ...

    def get_promos(self, login: typing.Optional[str]) -> dict:
        """Fetch `login` promotions."""
        ...

    def get_notifications(self, login: typing.Optional[str]) -> dict:
        """Retrieve `login` recent notifications."""
        ...

    def get_current_activities(self, login: typing.Optional[str]) -> dict:
        """Fetch `login` current activities."""
        ...
