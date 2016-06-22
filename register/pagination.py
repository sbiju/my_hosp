from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class PaymentPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 3
    limit_query_param = 'limit'
    offset_query_param = 'offset'


class PatientPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 3
    limit_query_param = 'limit'
    offset_query_param = 'offset'
