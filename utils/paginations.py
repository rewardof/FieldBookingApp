from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DynamicPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Query parameter for custom page size
    max_page_size = 100  # Maximum page size allowed

    def get_page_size(self, request):
        if self.page_size_query_param in request.query_params:
            try:
                page_size = int(request.query_params[self.page_size_query_param])
                if page_size > 0:
                    return page_size
            except ValueError:
                pass
        return self.page_size

    def get_paginated_response(self, data):
        return Response(self.get_paginated_data(data))

    def get_paginated_data(self, data):
        return {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        }
