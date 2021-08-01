from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from rest_framework.response import Response


class LargeResultsSetPagination(PageNumberPagination):
    _ = 10
    if settings.TEST:
        _ = 1
    page_size = _
    page_size_query_param = "page_size"
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    _ = 10
    if settings.TEST:
        _ = 1
    page_size = _
    page_size_query_param = "page_size"
    max_page_size = 1000
