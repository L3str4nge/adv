import uuid
from typing import Type
from datetime import datetime
from django.db import models
import petl

from adv.core.exceptions import InvalidStorageType
from adv.core.integration import BaseIntegration
from adv.datasets.exceptions import InvalidCountByParam
from adv.core.storage import Storage
from adv.core.utils import find_integration_by_name, get_loader_for_file

import logging

log = logging.getLogger(__name__)


class Dataset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField()
    created = models.DateTimeField(default=datetime.now, blank=True)
    name = models.CharField(max_length=10, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)

    @classmethod
    def from_integration(cls, name, storage_type: str = "csv"):
        integration_class: Type[BaseIntegration] = find_integration_by_name(name)

        storage = Storage.get(storage_type)

        if not storage:
            raise InvalidStorageType(f"{storage_type} is not supported type")

        for data in integration_class().collect_and_transform():
            storage.write(data)

        content_file = storage.get_content_file(encoding="utf-8")

        instance = cls(name=name)
        instance.save()
        instance.file.save(f"{instance}.csv", content_file)
        return instance

    def get_dataset_content(self, params: dict):
        if 'count_by' in params:
            headers, rows = self.get_countable_dataset_rows(params)
        else:
            headers, rows = self.get_default_dataset_rows(params)

        return {
            "headers": headers,
            "rows": rows
        }

    def get_countable_dataset_rows(self, params: dict):
        log.info(f"Getting countable dataset rows for params {params}")
        loader = get_loader_for_file(self.file)
        table = loader(self.file)
        headers = list(petl.header(table))

        count_by_fields = params.get("count_by").split(',')

        if not any(count_by_fields):
            raise InvalidCountByParam("count_by param cannot be empty")

        if not set(count_by_fields) <= set(headers):
            raise InvalidCountByParam("Provided unsupported count_by param")

        counted_table = petl.util.counting.valuecounts(table, *count_by_fields)
        headers = petl.header(counted_table)
        rows = list(petl.records(counted_table))
        return headers, rows

    def get_default_dataset_rows(self, params: dict):
        starts_from = int(params.get("starts_from", 0))

        if starts_from < 0:
            raise ValueError("starts_from parameter cannot be < 0")

        loader = get_loader_for_file(self.file)
        table = loader(self.file)

        headers = list(petl.header(table))
        rows = list(petl.records(table, starts_from, starts_from + 10))

        return headers, rows

    def get_dataset_headers(self):
        loader = get_loader_for_file(self.file)
        table = loader(self.file)
        return list(petl.header(table))
