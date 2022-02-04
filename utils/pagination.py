from rest_framework import pagination

from utils.response import successful_response


DEFAULT_PAGE_SIZE = 20


class PlannerPagination(pagination.PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return successful_response(
            data=data,
            pagination={
                'current_page': self.page.number,
                'has_more_page': self.page.has_next(),
                'per_page': int(self.request.GET.get('page_size', self.page_size)),
                'total': self.page.paginator.count
            }
        )
