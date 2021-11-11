from django.core.files.base import ContentFile

from adv.core.storage import Storage, CSVStorage


def test_storage_factory_valid_type():
    assert isinstance(Storage.get("csv"), CSVStorage)
    assert isinstance(Storage.get("cSv"), CSVStorage)
    assert isinstance(Storage.get("CSV"), CSVStorage)
    assert isinstance(Storage.get("CsV"), CSVStorage)


def test_storage_factory_invalid_type():
    assert not Storage.get("not_existing_type")


def test_csv_storage_write():
    storage = CSVStorage()
    storage.write([1, 1, 1])

    assert storage.buffer.getvalue() == '1,1,1\r\n'


def test_csv_writer_get_content_file():
    storage = CSVStorage()
    storage.write([1, 1, 1])

    content_file = storage.get_content_file("utf8")
    assert isinstance(content_file, ContentFile)
    assert content_file.readlines() == [b'1,1,1\r\n']
