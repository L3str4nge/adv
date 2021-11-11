import pytest

from adv.swapi.client import SWAPIConnector
from adv.swapi.integration import SWAPI


@pytest.fixture
def swapi_connector():
    connector = SWAPIConnector()
    connector.ENDPOINT = "test_endpoint"
    connector.BASE_URL = "https://test_base_url.com"
    return connector


@pytest.fixture
def planets_response():
    return [{"url": f"test_{i}", "name": f"test_{i}"} for i in range(10)]


@pytest.fixture
def integration_with_planets():
    swapi = SWAPI()
    swapi.planets = {"test_url_1": "test_1", "test_url_2": "test_2"}
    return swapi
