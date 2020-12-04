from core.response import Response
from utils.debug import Debug


class ResponseMixin():
    """
    For Custom Response

    Mostly copy of rest_framework mixins.
    Check rest_framework/mixins.py
    """

    def _check_ownership(self, request, instance):
        user = request.user
        if user.is_staff:
            return True
        elif hasattr(instance, 'user') and user == instance.user:
            return True
        else:
            return False

    def set_serializer(self, serializer_class, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        Debug.trace(request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=Response.HTTP_201,
            headers=headers
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        Debug.trace(request.data)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        Debug.trace(
            'Destroying %s' % instance
        )
        self.perform_destroy(instance)
        return Response(status=Response.HTTP_204)
