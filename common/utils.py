from rest_framework.pagination import PageNumberPagination


class BlogPaginator(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'per_page'
    max_page_size = 100
