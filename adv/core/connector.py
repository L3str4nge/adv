from abc import ABCMeta, abstractmethod
from typing import Generator


class BaseConnector(metaclass=ABCMeta):
    """ Base class for creating connectors to the integration API.

    This class provides two abstract methods for paginated responses.

    'fetch_all' method returns Generator because the collecting and processing data from api should be executing
    set by set instead of fetching large amount of data at once.

    'fetch_single_page' is optional if you will use API which does not support pagination at all.
    """
    ENDPOINT = ""
    BASE_URL = ""

    @abstractmethod
    def fetch_all(self) -> Generator:
        ...

    @abstractmethod
    def fetch_single_page(self, url: str) -> dict:
        ...
