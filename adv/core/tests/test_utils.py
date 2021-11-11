from unittest.mock import MagicMock

import petl
from django.conf import settings
from unittest import mock

from django.core.exceptions import ValidationError

from adv.core.exceptions import IntegrationNotFound
from adv.core.utils import find_integration_by_name, get_loader_for_file
import pytest


@mock.patch("adv.core.utils.import_string")
def test_find_integration_by_name(import_string_mock):
    mock_class = MagicMock()
    mock_class.name = "TEST"
    import_string_mock.return_value = mock_class
    settings.INTEGRATIONS = ["TEST.MODULE"]

    assert find_integration_by_name("TEST")


def test_find_integration_by_name_not_found():
    settings.INTEGRATIONS = []

    with pytest.raises(IntegrationNotFound):
        find_integration_by_name("NOT_FOUND")


@mock.patch("adv.core.utils.import_string")
def test_find_integration_found_but_name_incorrect(import_string_mock):
    mock_class = MagicMock()
    mock_class.name = "TEST"
    import_string_mock.return_value = mock_class
    settings.INTEGRATIONS = ["TEST.MODULE"]

    with pytest.raises(IntegrationNotFound):
        find_integration_by_name("BAD_NAME")


def test_loader_for_supported_file():
    file_mock = MagicMock()
    file_mock.name = "test.csv"

    assert get_loader_for_file(file_mock) == petl.fromcsv


def test_loader_for_unsupported_file():
    file_mock = MagicMock()
    file_mock.name = "test.zippedjpeg"

    with pytest.raises(ValidationError):
        get_loader_for_file(file_mock)
