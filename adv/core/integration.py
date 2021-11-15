from abc import ABCMeta, abstractmethod
from typing import Generator


class BaseIntegration(metaclass=ABCMeta):
    """Base class for creating API integrations

    This class is the common interface for API's which return datasets we want to process and save in DB.
    The main functionality is to process a data in stream approach one by one:

    1. Collect bunch of data
    2. Transform it
    3. Pass it trough to the next operations (eg. save as CSV or save into DB)
    """
    name = ""

    @abstractmethod
    def collect(self) -> Generator:
        ...

    @abstractmethod
    def transform(self, data: dict) -> Generator:
        ...

    def collect_and_transform(self) -> Generator:
        for collected_data in self.collect():
            yield from self.transform(collected_data)
