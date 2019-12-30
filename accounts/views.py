from rest_framework.generics import CreateAPIView

from core.permissions import (
    AllowAny,
)
from core.mixins import ResponseMixin
from utils.debug import Debug  # noqa

from . import serializers


class UserSignupView(ResponseMixin, CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = serializers.SignupSerializer
