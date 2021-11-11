from rest_framework import status
from rest_framework.decorators import api_view
import logging

from rest_framework.response import Response

from adv.datasets.models import Dataset
from adv.datasets.serializers import DatasetCreateSerializer, DatasetSerializer, DatasetHeaderSerializer
from adv.datasets.views import get_dataset_or_raise_404

log = logging.getLogger(__name__)


@api_view(['POST'])
def create_dataset(request):
    if request.method == 'POST':
        log.info(f"Create dataset for {request.data}")
        try:
            dataset = Dataset.from_integration(
                name=request.data["name"],
                storage_type=request.data.get("storage_type", "csv")
            )
        except Exception as e:
            msg = f"Could not create the dataset {e}"
            log.exception(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        serializer = DatasetCreateSerializer(dataset)
        return Response(serializer.data, status.HTTP_201_CREATED)


@api_view(['GET'])
def load_dataset(request, uuid):
    if request.method == 'GET':
        log.info(f"Get details for dataset {uuid}")
        dataset_obj = get_dataset_or_raise_404(uuid)
        try:
            content = dataset_obj.get_dataset_content(params=request.query_params)
        except Exception as e:
            msg = f"Could not load the dataset details {e}"
            log.exception(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        serializer = DatasetSerializer({"dataset": dataset_obj, "content": content})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def dataset_headers(request, uuid):
    if request.method == 'GET':
        log.info(f"Get headers for dataset {uuid}")
        dataset_obj = get_dataset_or_raise_404(uuid)
        try:
            headers = dataset_obj.get_dataset_headers()
        except Exception as e:
            msg = f"Could not load the dataset headers {e}"
            log.exception(msg)
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

        serializer = DatasetHeaderSerializer({"dataset": dataset_obj, "headers": headers})
        return Response(serializer.data, status=status.HTTP_200_OK)
