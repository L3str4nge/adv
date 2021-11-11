from unittest.mock import patch, MagicMock

import pytest

from adv.swapi.exception import SWAPIConnectorError


def test_connector_get_url_for_page(swapi_connector):
    url_for_page_1 = swapi_connector.get_url_for_page(1)
    assert url_for_page_1 == "https://test_base_url.com/test_endpoint/?page=1"

    url_for_page_2 = swapi_connector.get_url_for_page(2)
    assert url_for_page_2 == "https://test_base_url.com/test_endpoint/?page=2"

    url_for_page_999 = swapi_connector.get_url_for_page(999)
    assert url_for_page_999 == "https://test_base_url.com/test_endpoint/?page=999"

    with pytest.raises(AssertionError):
        swapi_connector.get_url_for_page(-2)


@patch("requests.get")
def test_connector_fetch_single_page_success(get_mock, swapi_connector):
    get_mock.return_value = MagicMock()
    swapi_connector.fetch_single_page(1)


@patch("requests.get")
def test_connector_fetch_single_page_raises_an_error(get_mock, swapi_connector):
    get_mock.return_value = Exception("Test exception")

    with pytest.raises(SWAPIConnectorError):
        swapi_connector.fetch_single_page(1)


@patch("adv.swapi.client.SWAPIConnector.fetch_single_page")
def test_fetch_all_api_only_one_page(fetch_single_page_mock, swapi_connector):
    fetch_single_page_mock.return_value = {"test": "test"}

    for _ in swapi_connector.fetch_all():
        pass

    assert fetch_single_page_mock.call_count == 1


@patch("adv.swapi.client.SWAPIConnector.fetch_single_page")
def test_fetch_all_api_with_next_page(fetch_single_page_mock, swapi_connector):
    fetch_single_page_mock.return_value = {"next": "test"}
    fetch_all = swapi_connector.fetch_all()

    next(fetch_all)
    next(fetch_all)
    next(fetch_all)

    fetch_single_page_mock.return_value = {}  # stop the iteration
    next(fetch_all)

    assert fetch_single_page_mock.call_count == 4


@patch("requests.get")
def test_fetch_all_fetch_single_page_raise_an_error(get_mock, swapi_connector):
    get_mock.side_effect = Exception("Test")

    with pytest.raises(SWAPIConnectorError):
        for _ in swapi_connector.fetch_all():
            pass
