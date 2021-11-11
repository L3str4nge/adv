from typing import Generator

import requests
from django.conf import settings
import logging

from adv.core.connector import BaseConnector
from adv.swapi.exception import SWAPIConnectorError

log = logging.getLogger(__name__)


class SWAPIConnector(BaseConnector):
    """Connector class for SWAPI API

    It does traverse entire paginated API and yields results one by one.
    It's used as a base class for particular endpoints like /people or /planets
    """
    ENDPOINT = ""
    BASE_URL = settings.SWAPI_BASE_URL

    def fetch_all(self) -> Generator:
        """Fetches all pages based on `next` url in response.

        Yield each fetched response to be processed immediately.

        This class would be a core base class if we will have more APIs to handle.
        """
        initial_url = self.get_url_for_page(page=1)
        log.info(f"Fetching data from {initial_url}")
        response = self.fetch_single_page(initial_url)
        yield response

        next_url = response.get("next")
        while next_url:
            response = self.fetch_single_page(next_url)
            yield response
            next_url = response.get("next")

    def fetch_single_page(self, url: str) -> dict:
        log.info(f"Fetching {url}...")
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            msg = f"Cannot fetch {url}"
            log.exception(msg, exc_info=e)
            raise SWAPIConnectorError(msg)

        return response.json()

    def get_url_for_page(self, page: int = 1):
        assert page > 0
        return f"{self.BASE_URL}/{self.ENDPOINT}/?page={page}"


class PeopleConnector(SWAPIConnector):
    ENDPOINT = "people"


class PlanetsConnector(SWAPIConnector):
    ENDPOINT = "planets"
