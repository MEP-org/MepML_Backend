from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 6

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total': self.page.paginator.count,
            'this_page': len(self.page.paginator.object_list),
            'results': data
        })