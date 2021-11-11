from unittest.mock import patch, MagicMock

from adv.core.exceptions import InvalidStorageType
from adv.datasets.exceptions import InvalidCountByParam
from adv.datasets.models import Dataset
import pytest


@patch("adv.datasets.models.find_integration_by_name")
def test_from_integration(find_integration_mock):
    find_integration_mock.return_value = MagicMock()

    instance = Dataset.from_integration("test")
    assert instance
    assert instance.file
    assert instance.name == "test"


@patch("adv.datasets.models.find_integration_by_name")
def test_from_integration_bad_storage_type(find_integration_mock):
    find_integration_mock.return_value = MagicMock()

    with pytest.raises(InvalidStorageType):
        Dataset.from_integration("test", storage_type="test")


@patch("adv.datasets.models.Dataset.get_default_dataset_rows")
@patch("adv.datasets.models.Dataset.get_countable_dataset_rows")
def test_dataset_rows_with_count_by(countable_mock, default_mock, dataset):
    countable_mock.return_value = ("test", "test")
    dataset.get_dataset_content({'count_by': "test"})

    assert countable_mock.called
    assert not default_mock.called


@patch("adv.datasets.models.Dataset.get_default_dataset_rows")
@patch("adv.datasets.models.Dataset.get_countable_dataset_rows")
def test_dataset_rows_default(countable_mock, default_mock, dataset):
    default_mock.return_value = "test", "test"
    dataset.get_dataset_content({})

    assert not countable_mock.called
    assert default_mock.called


@patch("adv.datasets.models.get_loader_for_file")
def test_dataset_headers(get_loader_mock, dataset, dummy_table):
    loader_mock = MagicMock()
    loader_mock.return_value = dummy_table
    get_loader_mock.return_value = loader_mock

    assert dataset.get_dataset_headers() == ["foo", "bar"]


@patch("adv.datasets.models.get_loader_for_file")
def test_get_default_dataset_rows(get_loader_mock, dataset, dummy_table):
    loader_mock = MagicMock()
    loader_mock.return_value = dummy_table
    get_loader_mock.return_value = loader_mock

    headers, rows = dataset.get_default_dataset_rows({})
    assert headers == ["foo", "bar"]
    assert rows == [(i, i) for i in range(0, 10)]

    headers, rows = dataset.get_default_dataset_rows({"starts_from": 10})
    assert headers == ["foo", "bar"]
    assert rows == [(i, i) for i in range(10, 20)]

    headers, rows = dataset.get_default_dataset_rows({"starts_from": 45})
    assert headers == ["foo", "bar"]
    assert rows == [(i, i) for i in range(45, 55)]

    headers, rows = dataset.get_default_dataset_rows({"starts_from": 99})
    assert headers == ["foo", "bar"]
    assert rows == [(i, i) for i in range(99, 100)]

    headers, rows = dataset.get_default_dataset_rows({"starts_from": 834821312})
    assert headers == ["foo", "bar"]
    assert rows == []


@patch("adv.datasets.models.get_loader_for_file")
def test_get_default_dataset_rows_starts_from_less_than_0(get_loader_mock, dataset, loader_mock_with_table):
    get_loader_mock.return_value = loader_mock_with_table

    with pytest.raises(ValueError):
        dataset.get_default_dataset_rows({"starts_from": -10})


@patch("adv.datasets.models.get_loader_for_file")
def test_get_countable_dataset_rows_empty_count_by(get_loader_mock, dataset, loader_mock_with_table):
    get_loader_mock.return_value = loader_mock_with_table

    with pytest.raises(InvalidCountByParam):
        dataset.get_countable_dataset_rows({"count_by": ""})


@patch("adv.datasets.models.get_loader_for_file")
def test_get_countable_dataset_rows_not_existing_count_by(get_loader_mock, dataset, loader_mock_with_table):
    get_loader_mock.return_value = loader_mock_with_table

    with pytest.raises(InvalidCountByParam):
        dataset.get_countable_dataset_rows({"count_by": "foo,test2"})


@patch("adv.datasets.models.get_loader_for_file")
def test_get_countable_dataset_rows_existing_count_by(get_loader_mock, dataset, loader_mock_with_table):
    get_loader_mock.return_value = loader_mock_with_table

    headers, rows = dataset.get_countable_dataset_rows({"count_by": "foo,bar"})
    assert headers == ("foo", "bar", "count", "frequency")
    assert rows == [(i, i, 1, 0.01) for i in range(0, 100)]

    headers, rows = dataset.get_countable_dataset_rows({"count_by": "foo"})
    assert headers == ("foo", "count", "frequency")
    assert rows == [(i,  1, 0.01) for i in range(0, 100)]

    headers, rows = dataset.get_countable_dataset_rows({"count_by": "bar"})
    assert headers == ("bar", "count", "frequency")
    assert rows == [(i,  1, 0.01) for i in range(0, 100)]
