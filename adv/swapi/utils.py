from typing import Generator

from .client import PlanetsConnector


def collect_planets() -> Generator:
    for data in PlanetsConnector().fetch_all():
        yield from data["results"]


def collect_and_create_planets_map() -> dict:
    planets_map = {planet["url"]: planet["name"] for planet in collect_planets()}
    return planets_map
