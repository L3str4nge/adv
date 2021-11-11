import csv
from io import StringIO
from django.core.files.base import ContentFile


class CSVStorage:
    def __init__(self):
        self.buffer = StringIO()
        self.writer = csv.writer(self.buffer)

    def write(self, data: list):
        self.writer.writerow(data)

    def get_content_file(self, encoding) -> ContentFile:
        return ContentFile(self.buffer.getvalue().encode(encoding))


class Storage:
    """ Factory which returns object responsible for writing data for a given type of storage."""
    STORAGES = {
        "csv": CSVStorage
    }

    @classmethod
    def get(cls, _type: str):
        if _type.lower() not in cls.STORAGES:
            return None

        return cls.STORAGES.get(_type.lower())()
