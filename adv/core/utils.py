from typing import Callable

import petl
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile
from django.utils.module_loading import import_string

from adv.core.exceptions import IntegrationNotFound


def find_integration_by_name(name: str):
    """ Getting integration class from settings and search class for a given name."""
    for integration_path in settings.INTEGRATIONS:
        _class = import_string(integration_path)

        if hasattr(_class,  "name") and _class.name == name:
            return _class

    raise IntegrationNotFound(f"Integration {name} is not defined or badly configured.")


def get_loader_for_file(file: FieldFile) -> Callable:
    """ Returns loader function for a given type of file."""
    if file.name.endswith('.csv'):
        return petl.fromcsv

    raise ValidationError(f"{file.name} extension is not supported")
