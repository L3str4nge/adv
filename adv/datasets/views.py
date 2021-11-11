import logging

from django.http import Http404
from django.shortcuts import render

from adv.datasets.models import Dataset

log = logging.getLogger(__name__)


def get_dataset_or_raise_404(uuid):
    try:
        return Dataset.objects.get(id=uuid)
    except Dataset.DoesNotExist:
        raise Http404("Dataset does not exist")


def index(request):
    datasets = Dataset.objects.all()  # should be paginated in the future as well
    return render(request, "index.html", {"datasets": datasets})


def dataset(request, uuid):
    dataset = get_dataset_or_raise_404(uuid)
    return render(request, "dataset.html", {"dataset": dataset})


def value_count(request, uuid):
    dataset = get_dataset_or_raise_404(uuid)
    return render(request, "value_count.html", {"dataset": dataset})
