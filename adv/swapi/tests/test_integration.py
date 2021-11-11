from unittest.mock import patch

from adv.swapi.integration import SWAPI


def test_swapi_header_fields():
    assert SWAPI.FIELDS == [
        "name",
        "height",
        "mass",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "gender",
        "homeworld",
        "date"
    ]


@patch("adv.swapi.integration.SWAPI._create_date_field")
@patch("adv.swapi.integration.SWAPI._transform_homeworld")
@patch("adv.swapi.integration.SWAPI._drop_fields")
def test_transform_flow(drop_fields, transform_homeworld, create_date_field):
    transform = SWAPI().transform({"data": "test"})

    result = list(next(transform))

    assert result == ["test"]
    assert create_date_field.called
    assert transform_homeworld.called
    assert drop_fields.called


def test_create_date_field_valid_format():
    data = {"edited": "2021-11-15T08:40:25.1232Z"}
    SWAPI()._create_date_field(data)

    assert data["date"] == "2021-11-15"


def test_create_date_field_invalid_format():
    data = {"edited": "2021-11-15T08:40:25"}
    SWAPI()._create_date_field(data)

    assert data["date"] == "2021-11-15T08:40:25"


def test_create_date_field_edited_does_not_exist():
    data = {}
    SWAPI()._create_date_field(data)

    assert data["date"] == "unknown"


def test_transform_homeworld_transform_success(integration_with_planets):
    swapi = integration_with_planets
    data = {"homeworld": "test_url_1"}
    swapi._transform_homeworld(data)

    assert data["homeworld"] == "test_1"


def test_transform_homeworld_does_not_exist(integration_with_planets):
    swapi = integration_with_planets
    data = {"homeworld": "test_url_9999"}
    swapi._transform_homeworld(data)

    assert data["homeworld"] == "unknown"


def test_transform_homeworld_data_without_homeworld_key(integration_with_planets):
    swapi = integration_with_planets
    data = {}
    swapi._transform_homeworld(data)

    assert data["homeworld"] == "unknown"


def test_drop_fields_that_does_not_belong():
    data = {"key_1": 1, "key_2": 2}

    SWAPI()._drop_fields(data)

    assert data == {}


def test_drop_fields_that_belongs():
    data = {"key_1": 1, "key_2": 2}
    swapi = SWAPI()
    swapi.FIELDS = list(data.keys())

    swapi._drop_fields(data)

    assert len(data) == 2
    assert list(data.keys()) == ["key_1", "key_2"]
