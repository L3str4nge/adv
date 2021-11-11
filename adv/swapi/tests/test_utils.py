from unittest.mock import patch

from adv.swapi.utils import collect_and_create_planets_map


@patch("adv.swapi.utils.collect_planets")
def test_collect_and_create_planets_map(collect_planets_mock, planets_response):
    collect_planets_mock.return_value = planets_response
    planets_map = collect_and_create_planets_map()

    assert planets_map == {f"test_{i}": f"test_{i}" for i in range(10)}


@patch("adv.swapi.utils.collect_planets")
def test_collect_and_create_planets_map_empty_response(collect_planets_mock):
    collect_planets_mock.return_value = []
    planets_map = collect_and_create_planets_map()

    assert planets_map == {}
