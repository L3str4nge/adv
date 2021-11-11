from unittest.mock import MagicMock

import pytest

from adv.datasets.models import Dataset


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def dataset():
    return Dataset.objects.create(name="dummy")


@pytest.fixture
def dummy_table():
    table = [["foo", "bar"]]
    for i in range(100):
        table.append([i, i])
    return table


@pytest.fixture
def loader_mock_with_table(dummy_table):
    loader_mock = MagicMock()
    loader_mock.return_value = dummy_table
    return loader_mock
