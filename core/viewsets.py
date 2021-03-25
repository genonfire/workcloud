from rest_framework.generics import (
    CreateAPIView as _CreateAPIView,
    GenericAPIView as _GenericAPIView
)
from rest_framework.views import APIView as _APIView
from rest_framework.viewsets import (
    GenericViewSet as _GenericViewSet,
    ModelViewSet as _ModelViewSet,
    ReadOnlyModelViewSet as _ReadOnlyModelViewSet
)

from core.response import Response
from core.mixins import (ResponseMixin)
from utils.debug import Debug


class APIView(_APIView):
    http_method_names = ['post']


class CreateAPIView(
    ResponseMixin, _CreateAPIView
):  # lgtm [py/conflicting-attributes]
    http_method_names = ['post']


class GenericAPIView(
    ResponseMixin, _GenericAPIView
):  # lgtm [py/conflicting-attributes]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        Debug.trace(request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=Response.HTTP_200)


class GenericViewSet(
    ResponseMixin, _GenericViewSet
):  # lgtm [py/conflicting-attributes]
    pass


class ModelViewSet(
    ResponseMixin, _ModelViewSet
):  # lgtm [py/conflicting-attributes]
    pass


class ReadOnlyModelViewSet(
    ResponseMixin, _ReadOnlyModelViewSet
):  # lgtm [py/conflicting-attributes]
    pass
