from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 6

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current_page': self.page.number, # Current page
            'total_pages': self.page.paginator.num_pages, # Total quantity of pages
            'total_elements': self.page.paginator.count, # Quantity of exercises in the database
            'this_page_elements': len(self.page.paginator.object_list), # Quantity of exercises in this page
            'results': data,
        })