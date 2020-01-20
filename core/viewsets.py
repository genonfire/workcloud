from rest_framework.generics import (
    CreateAPIView as _CreateAPIView,
    GenericAPIView as _GenericAPIView
)
from rest_framework.viewsets import (
    GenericViewSet as _GenericViewSet,
    ModelViewSet as _ModelViewSet,
    ReadOnlyModelViewSet as _ReadOnlyModelViewSet
)

from core.mixins import ResponseMixin


class CreateAPIView(ResponseMixin, _CreateAPIView):
    pass


class GenericAPIView(ResponseMixin, _GenericAPIView):
    pass


class GenericViewSet(ResponseMixin, _GenericViewSet):
    pass


class ModelViewSet(ResponseMixin, _ModelViewSet):
    pass


class ReadOnlyModelViewSet(ResponseMixin, _ReadOnlyModelViewSet):
    pass
