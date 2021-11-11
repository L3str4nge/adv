from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from .api import views as api_views

urlpatterns = [
    path("", views.index, name="dataset_list"),
    path('dataset/<uuid:uuid>/', views.dataset, name="dataset_details"),
    path('dataset/<uuid:uuid>/value-count/', views.value_count, name="value_count"),

    path('api/dataset/', api_views.create_dataset, name="dataset_create"),
    path('api/dataset/<uuid:uuid>/', api_views.load_dataset, name="load_dataset"),
    path('api/dataset/<uuid:uuid>/headers', api_views.dataset_headers, name="get_headers"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
