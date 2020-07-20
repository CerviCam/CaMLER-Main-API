from rest_framework.pagination import LimitOffsetPagination

class DefaultLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10