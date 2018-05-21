from rest_framework.pagination import PageNumberPagination

__author__ = 'richard'


class ThreePagination(PageNumberPagination):
    page_size = 3

class TenPagination(PageNumberPagination):
    page_size = 10