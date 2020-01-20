from collections import OrderedDict
from math import ceil

from django.core.paginator import InvalidPage

from rest_framework.exceptions import NotFound
from rest_framework.pagination import (
    _positive_int,
    PageNumberPagination as _BasePagination
)
from rest_framework.response import Response

from utils.constants import Const


class PageNumberPagination(_BasePagination):
    """
    Pagination Style

    Check https://www.django-rest-framework.org/api-guide/pagination/
    """

    page_size_query_param = 'page_size'

    link_count = Const.DEFAULT_LINK_COUNT
    link_count_query_param = 'link_count'
    link_count_query_description = 'Number of links to pages per page.'
    max_link_count = None

    def get_link_count(self, request):
        if self.link_count_query_param:
            try:
                return _positive_int(
                    request.query_params.get(
                        self.link_count_query_param, self.link_count
                    ),
                    strict=True,
                    cutoff=self.max_link_count
                )
            except (KeyError, ValueError):
                pass

        return self.link_count

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if not page_size:
            return None
        if not self.get_link_count(request):
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        self.current_page = int(page_number)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data):
        item_total = self.page.paginator.count
        page_size = self.page.paginator.per_page
        current_page = self.current_page
        link_count = self.link_count

        page_total = int(ceil(float(item_total) / page_size))
        page_from = int(current_page / link_count) * link_count + 1
        page_to = page_total
        if page_to - page_from >= link_count:
            page_to = page_from + link_count - 1

        return Response(OrderedDict([
            ('pagination', OrderedDict([
                ('item_total', item_total),
                ('page_total', page_total),
                ('page_from', page_from),
                ('page_to', page_to),
                ('current_page', current_page),
            ])),
            ('data', data)
        ]))
