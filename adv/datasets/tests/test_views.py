import pytest
from django.http import Http404
from django.urls import reverse
import uuid

from adv.datasets.models import Dataset
from adv.datasets.views import get_dataset_or_raise_404


def test_dataset_or_raise_404_found(dataset):
    obj = get_dataset_or_raise_404(dataset.id)

    assert obj
    assert obj.id == dataset.id


def test_dataset_or_raise_404_not_found():
    with pytest.raises(Http404):
        get_dataset_or_raise_404(uuid.uuid4())


def test_index_view_with_existing_object(client):
    Dataset.objects.create(name="dummy1")
    Dataset.objects.create(name="dummy2")
    Dataset.objects.create(name="dummy3")
    Dataset.objects.create(name="dummy4")

    response = client.get(reverse("dataset_list"))

    assert response.status_code == 200

    dataset_qs = response.context.dicts[-1]["datasets"]
    assert dataset_qs.count() == 4


def test_index_view_with_empty_db(client):
    response = client.get(reverse("dataset_list"))

    assert response.status_code == 200

    dataset_qs = response.context.dicts[-1]["datasets"]
    assert dataset_qs.count() == 0


def test_dataset_details(client, dataset):
    response = client.get(reverse("dataset_details", kwargs={"uuid": dataset.id}))
    assert response.status_code == 200
    assert response.context.dicts[-1]["dataset"].id == dataset.id


def test_dataset_details_not_found(client):
    response = client.get(reverse("dataset_details", kwargs={"uuid": uuid.uuid4()}))
    assert response.status_code == 404


def test_value_count(client, dataset):
    response = client.get(reverse("value_count", kwargs={"uuid": dataset.id}))
    assert response.status_code == 200
    assert response.context.dicts[-1]["dataset"].id == dataset.id


def test_value_count_not_found(client):
    response = client.get(reverse("value_count", kwargs={"uuid": uuid.uuid4()}))
    assert response.status_code == 404
