from typing import Generator
import logging
import petl

from adv.core.integration import BaseIntegration
from adv.swapi.client import PeopleConnector
from adv.swapi.utils import collect_and_create_planets_map

log = logging.getLogger(__name__)


class SWAPI(BaseIntegration):
    """ Class responsible for collecting and transforming data retrieved from SWAPI API

    This implementation based on dict data getting from response.json() while fetching.
    It would be better to use petl 'fromdicts()' function here and operate directly on petl's table
    but I had troubles here to get things done so I decided to left  it native.
    """
    name = "swapi"
    planets: dict
    FIELDS = [
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
        "date"
    ]

    def collect(self) -> Generator:
        log.info("Creating planets map...")
        self.planets = collect_and_create_planets_map()

        log.info("Collecting people...")
        for data in PeopleConnector().fetch_all():
            yield from data["results"]

    def transform(self, data: dict) -> Generator:
        log.info("Transforming collected data...")

        self._create_date_field(data)
        self._transform_homeworld(data)
        self._drop_fields(data)
        yield data.values()

    def _create_date_field(self, data: dict):
        isodatetime = petl.datetimeparser('%Y-%m-%dT%H:%M:%S.%fZ')

        if "edited" not in data:
            log.warning("There is no edited field in response. Setting value to unknown.")
            data["date"] = "unknown"
            return

        try:
            transformed_date = isodatetime(data["edited"]).strftime("%Y-%m-%d")
        except ValueError as e:
            log.exception(f"Invalid date format {e}. Setting date to original value.")
            transformed_date = data["edited"]

        data["date"] = transformed_date

    def _transform_homeworld(self, data: dict):
        if "homeworld" not in data:
            log.warning("There is no homeworld field in response. Setting value to unknown.")
            data["homeworld"] = "unknown"
            return

        data["homeworld"] = self.planets.get(data["homeworld"], "unknown")

    def _drop_fields(self, data: dict):
        """ Drop fields from data which does not belong to the self.FIELDS """
        for key in list(data.keys()):
            if key not in self.FIELDS:
                data.pop(key, None)

    def collect_and_transform(self):
        yield self.FIELDS  # yield headers first
        yield from super().collect_and_transform()
