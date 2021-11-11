from unittest.mock import patch, MagicMock

import uuid
from django.urls import reverse

from adv.datasets.models import Dataset


def test_create_dataset_bad_integration(client):
    response = client.post(reverse("dataset_create"), {"name": "bad_name"})
    assert response.status_code == 400


@patch("adv.datasets.models.find_integration_by_name")
def test_create_dataset_bad_storage(_, client):
    response = client.post(reverse("dataset_create"), {"name": "name", "storage_type": "not_existing"})
    assert response.status_code == 400


@patch("adv.datasets.models.find_integration_by_name")
def test_create_dataset_collect_and_transform_error(find_integration_mock, client):
    integration_class = MagicMock()
    integration_class().collect_and_transform.side_effect = Exception("Test")
    find_integration_mock.return_value = integration_class
    response = client.post(reverse("dataset_create"), {"name": "name", "storage_type": "csv"})
    assert response.status_code == 400


@patch("adv.datasets.models.find_integration_by_name")
def test_create_dataset_collect_and_transform_success(find_integration_mock, client, dummy_table):
    integration_class = MagicMock()
    integration_class().collect_and_transform.return_value = dummy_table
    find_integration_mock.return_value = integration_class
    response = client.post(reverse("dataset_create"), {"name": "name", "storage_type": "csv"})

    assert response.status_code == 201

    obj = Dataset.objects.last()
    response_json = response.json()

    assert obj.name == "name"
    assert obj.file
    assert str(obj.id) == response_json["id"]
    assert obj.created.strftime('%Y-%m-%dT%H:%M:%S.%fZ') == response_json["created"]


def test_load_dataset_not_found(client):
    response = client.get(reverse("load_dataset", kwargs={"uuid": uuid.uuid4()}))
    assert response.status_code == 404


@patch("adv.datasets.models.get_loader_for_file")
def test_load_dataset_raises_an_error(file_loader_mock, dataset, client):
    file_loader_mock.side_effect = Exception("Test exception")
    response = client.get(reverse("load_dataset", kwargs={"uuid": dataset.id}))
    assert response.status_code == 400


@patch("adv.datasets.models.get_loader_for_file")
def test_load_dataset_countable_dataset_rows(get_loader_mock, loader_mock_with_table, client, dataset):
    get_loader_mock.return_value = loader_mock_with_table
    response = client.get(reverse("load_dataset", kwargs={"uuid": dataset.id}), data={"count_by": "foo"})

    assert response.status_code == 200

    content = response.json()["content"]
    assert content["headers"] == ["foo", "count", "frequency"]
    assert content["rows"] == [[i,  1, 0.01] for i in range(0, 100)]


@patch("adv.datasets.models.get_loader_for_file")
def test_dataset_countable_dataset_default(get_loader_mock, loader_mock_with_table, client, dataset):
    get_loader_mock.return_value = loader_mock_with_table
    response = client.get(reverse("load_dataset", kwargs={"uuid": dataset.id}), data={"starts_from": "10"})

    assert response.status_code == 200

    content = response.json()["content"]
    assert content["headers"] == ["foo", "bar"]
    assert content["rows"] == [[i,  i] for i in range(10, 20)]


@patch("adv.datasets.models.get_loader_for_file")
def test_dataset_countable_dataset_default_mixin_with_countable(
        get_loader_mock, loader_mock_with_table, client, dataset
):
    get_loader_mock.return_value = loader_mock_with_table
    response = client.get(reverse(
        "load_dataset",
        kwargs={"uuid": dataset.id}),
        data={"starts_from": "10", "count_by": "foo"}
    )

    assert response.status_code == 200

    content = response.json()["content"]
    assert content["headers"] == ["foo", "count", "frequency"]
    assert content["rows"] == [[i,  1, 0.01] for i in range(0, 100)]


def test_dataset_headers_not_found(client):
    response = client.get(reverse("get_headers", kwargs={"uuid": uuid.uuid4()}))
    assert response.status_code == 404


@patch("adv.datasets.models.get_loader_for_file")
def test_dataset_headers_raises_an_error(file_loader_mock, dataset, client):
    file_loader_mock.side_effect = Exception("Test exception")
    response = client.get(reverse("get_headers", kwargs={"uuid": dataset.id}))
    assert response.status_code == 400


@patch("adv.datasets.models.get_loader_for_file")
def test_dataset_headers_success(get_loader_mock, loader_mock_with_table, client, dataset):
    get_loader_mock.return_value = loader_mock_with_table
    response = client.get(reverse("get_headers", kwargs={"uuid": dataset.id}))

    assert response.status_code == 200

    content = response.json()
    assert content["headers"] == ["foo", "bar"]
