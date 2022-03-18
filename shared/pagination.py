from rest_framework import pagination


class CustomPageNumberPagination(pagination.PageNumberPagination):
    """Custom page number pagination."""

    page_size = 10 
    max_page_size = 10000
    page_size_query_param = 'page_size'

    def get_page_size(self, request):
        """Get page size."""
        # On certain pages, force custom/max page size.
        try:
            view = request.parser_context['view']
            if view.action in [
                'custom_page_size_view_1',
                'custom_page_size_view_2',
                # ...
                'custom_page_size_view_n',
            ]:
                return self.max_page_size
        except:
            pass

        return super(CustomPageNumberPagination, self).get_page_size(request)
